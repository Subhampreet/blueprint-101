/* Markdown to HTML. Uses `marked` when the CDN script loaded; otherwise a small
   built-in renderer that covers everything the notes use (headings, lists, tables,
   fenced code, blockquotes, images, links, inline HTML such as <details>). */
(function () {
  "use strict";

  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function inline(s) {
    var codes = [];
    s = s.replace(/`([^`]+)`/g, function (_, c) { codes.push("<code>" + esc(c) + "</code>"); return "\u0001" + (codes.length - 1) + "\u0001"; });
    // escape bare < and > that are not part of an HTML tag the notes use
    s = s.replace(/<(?!\/?(details|summary|br|kbd|b|i|em|strong|sub|sup|mark)\b)/g, "&lt;");
    s = s.replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g, '<img alt="$1" src="$2">');
    s = s.replace(/\[([^\]]+)\]\(([^)\s]+)\)/g, '<a href="$2">$1</a>');
    s = s.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
    s = s.replace(/(^|[^*\w])\*([^*\n]+)\*(?!\w)/g, "$1<em>$2</em>");
    s = s.replace(/(^|\W)_([^_\n]+)_(?!\w)/g, "$1<em>$2</em>");
    return s.replace(/\u0001(\d+)\u0001/g, function (_, i) { return codes[+i]; });
  }

  function splitRow(line) {
    return line.trim().replace(/^\||\|$/g, "").split("|").map(function (c) { return c.trim(); });
  }

  function list(lines, i) {
    // parse a (possibly nested) list starting at lines[i]; returns [html, nextIndex]
    var m = lines[i].match(/^(\s*)([-*]|\d+\.)\s+/);
    var indent = m[1].length, ordered = /\d/.test(m[2]);
    var html = ordered ? "<ol>" : "<ul>";
    while (i < lines.length) {
      var lm = lines[i].match(/^(\s*)([-*]|\d+\.)\s+(.*)$/);
      if (!lm || lm[1].length < indent) break;
      if (lm[1].length > indent) {
        var sub = list(lines, i);
        html = html.replace(/<\/li>$/, sub[0] + "</li>");
        i = sub[1];
        continue;
      }
      var text = lm[3];
      i++;
      while (i < lines.length && lines[i].trim() && !/^\s*([-*]|\d+\.)\s+/.test(lines[i]) && /^\s+/.test(lines[i])) {
        text += " " + lines[i].trim();
        i++;
      }
      html += "<li>" + inline(text) + "</li>";
    }
    return [html + (ordered ? "</ol>" : "</ul>"), i];
  }

  function fallback(md) {
    var lines = md.replace(/\r/g, "").split("\n"), out = [], i = 0, para = [];
    function flush() { if (para.length) { out.push("<p>" + inline(para.join(" ")) + "</p>"); para = []; } }
    while (i < lines.length) {
      var line = lines[i];
      if (/^```/.test(line)) {
        flush();
        var lang = line.slice(3).trim(), code = [];
        i++;
        while (i < lines.length && !/^```/.test(lines[i])) code.push(lines[i++]);
        i++;
        out.push('<pre><code class="language-' + esc(lang) + '">' + esc(code.join("\n")) + "</code></pre>");
        continue;
      }
      var h = line.match(/^(#{1,6})\s+(.*)$/);
      if (h) { flush(); out.push("<h" + h[1].length + ">" + inline(h[2]) + "</h" + h[1].length + ">"); i++; continue; }
      if (/^(-{3,}|\*{3,})\s*$/.test(line)) { flush(); out.push("<hr>"); i++; continue; }
      if (/^>\s?/.test(line)) {
        flush();
        var q = [];
        while (i < lines.length && /^>\s?/.test(lines[i])) q.push(lines[i++].replace(/^>\s?/, ""));
        out.push("<blockquote>" + fallback(q.join("\n")) + "</blockquote>");
        continue;
      }
      if (/^\|/.test(line) && i + 1 < lines.length && /^\|?\s*:?-{2,}/.test(lines[i + 1])) {
        flush();
        var head = splitRow(line), rows = [];
        i += 2;
        while (i < lines.length && /^\|/.test(lines[i])) rows.push(splitRow(lines[i++]));
        out.push("<table><thead><tr>" + head.map(function (c) { return "<th>" + inline(c) + "</th>"; }).join("") +
          "</tr></thead><tbody>" + rows.map(function (r) {
            return "<tr>" + r.map(function (c) { return "<td>" + inline(c) + "</td>"; }).join("") + "</tr>";
          }).join("") + "</tbody></table>");
        continue;
      }
      if (/^\s*([-*]|\d+\.)\s+/.test(line)) { flush(); var l = list(lines, i); out.push(l[0]); i = l[1]; continue; }
      if (/^<\/?(details|summary|div)/.test(line.trim())) { flush(); out.push(line.trim().replace(/<summary>(.*)<\/summary>/, function (_, s) { return "<summary>" + inline(s) + "</summary>"; })); i++; continue; }
      if (/^<!--/.test(line.trim())) { i++; continue; }
      if (!line.trim()) { flush(); i++; continue; }
      para.push(line.trim());
      i++;
    }
    flush();
    return out.join("\n");
  }

  window.Markdown = {
    toHtml: function (md) {
      if (window.marked && typeof window.marked.parse === "function") {
        return window.marked.parse(md, { gfm: true, breaks: false });
      }
      return fallback(md);
    },
    _fallback: fallback
  };
})();
