# Erdős Problem 369 — drafting inputs

- upstream state: **proved (Lean)**  
- machine verdict: **unconditional** (source plby)  
- formal_proof link allowed: **True** (unconditional + signed vsa_ required)

## Problem text (VERBATIM SOURCE — cite, do not rephrase)

```latex
<!DOCTYPE html>
<html>

<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta charset="UTF-8">

<title>369 | Erdős Problems</title>
<meta property="og:title" content="369 | Erdős Problems">
<link rel="icon" href="/static/favicon.ico">
<link rel="stylesheet" href="/static/style.css?v=733265cf">

<script>
document.addEventListener('click', (e) => {
  // Toggle reply form
  const toggle = e.target.closest('.reply-toggle');
  if (toggle) {
    const id = toggle.getAttribute('data-target');
    const form = document.getElementById(id);
    if (form) form.classList.toggle('hidden');
  }
  // Reply with quote
  const quoteBtn = e.target.closest('.reply-quote');
  if (quoteBtn) {
    const id = quoteBtn.getAttribute('data-target');
    const form = document.getElementById(id);
    if (!form) return;
    const ta = form.querySelector('textarea');
    const raw = quoteBtn.getAttribute('data-raw') || '';
    const quoted = raw.split('\n').map(l => '> ' + l).join('\n') + '\n\n';
    ta.value = quoted;
    form.classList.remove('hidden');
    ta.focus();
    const len = ta.value.length;
    ta.setSelectionRange(len, len);
  }
});
</script>

<!-- This creates the reference in the bibliography box. -->

<script>
function addNewBox(key, problem_id, shouldScroll = false) {
  const local_id = 'bib-container' + String(problem_id);
  const container = document.getElementById(local_id);
  if (!container) return;

  container.innerHTML = "";

  fetch(`/bibs/${encodeURIComponent(key)}`)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.text();
    })
    .then(html => {
      container.innerHTML = html;

      if (shouldScroll) {
        requestAnimationFrame(() => {
          container.scrollIntoView({
            behavior: "smooth",
            block: "start"
          });
        });
      }
    })
    .catch(err => {
      console.error("Failed to load bib:", err);
      container.textContent = "Unable to load reference.";

      if (shouldScroll) {
        container.scrollIntoView({
          behavior: "smooth",
          block: "start"
        });
      }
    });
}
</script>

<script>
const filledSVG = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="black" class="fav-icon">
  <path fill-rule="evenodd" d="M10.788 3.21c.448-1.077 1.976-1.077 2.424 0l2.082 5.006 5.404.434c1.164.093 1.636 1.545.749 2.305l-4.117 3.527 1.257 5.273c.271 1.136-.964 2.033-1.96 1.425L12 18.354 7.373 21.18c-.996.608-2.231-.29-1.96-1.425l1.257-5.273-4.117-3.527c-.887-.76-.415-2.212.749-2.305l5.404-.434 2.082-5.005Z" clip-rule="evenodd" />
</svg>
                `;
const outlineSVG = `
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" stroke="black" fill="white" class="fav-icon">
  <path stroke-linecap="round" stroke-linejoin="round" d="M11.48 3.499a.562.562 0 0 1 1.04 0l2.125 5.111a.563.563 0 0 0 .475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 0 0-.182.557l1.285 5.385a.562.562 0 0 1-.84.610l-4.725-2.885a.562.562 0 0 0-.586 0L6.982 20.54a.562.562 0 0 1-.840-.610l1.285-5.386a.563.563 0 0 0-.182-.557L3.041 10.385a.562.562 0 0 1 .321-.988l5.518-.442a.563.563 0 0 0 .475-.345L11.48 3.5Z" />
</svg>
                `;

document.addEventListener("click", async (e) => {
  const btn = e.target.closest(".fav-btn");
  if (!btn) return;

  e.preventDefault();
  const problemId = btn.dataset.problemId;

  try {
    const res = await fetch(`/forum/toggle_favourite/${problemId}`, { method: "POST" });
    const data = await res.json();

    btn.dataset.favourited = data.favourited ? "true" : "false";
    btn.innerHTML = data.favourited ? filledSVG : outlineSVG;
  } catch (err) {
    console.error("Toggle failed:", err);
  }
});
</script>

    
<script>
function addImageBox(X, problem_id, shouldScroll = true) {
  const local_id = 'image-container' + String(problem_id);
  const container = document.getElementById(local_id);
  if (!container) return;

  container.innerHTML = "";

  const newBox = document.createElement("div");

  const img = document.createElement("img");
  img.src = `/static/${encodeURIComponent(X)}.png`;
  img.className = "responsive-image";
  img.alt = String(X);

  newBox.appendChild(img);
  container.appendChild(newBox);

  if (shouldScroll) {
    requestAnimationFrame(() => {
      container.scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
    });
  }
}
</script>


<script>
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('searchForm');
  if (!form) return;
  form.addEventListener('submit', function (e) {
    const input = form.querySelector('.searchTerm');
    if (!input) return;
    const value = input.value.trim();
    if (!value) return;
    const path = '/search/' + encodeURIComponent(value);
    const inDual = window.location.pathname.startsWith("/dual");
    if (inDual) {
      e.preventDefault(); 
      const selected = document.querySelector('input[name="targetPanel"]:checked');
      const panel = selected ? selected.value : "left";
      const iframe = document.getElementById(`iframe-${panel}`);
      if (iframe) {
        const url = path.includes("?") ? path + "&embed=1" : path + "?embed=1";
        iframe.src = url;
        const box = document.querySelector(`#panel-${panel} input`);
        if (box) box.value = path;
      } else {
        window.location.href = path;
      }
    } else {
      form.action = path;
      form.method = "GET";
    }
  });
});
</script>

<script>
document.addEventListener('DOMContentLoaded', function() {
  if (window.location.pathname.startsWith("/dual")) return;

  var form = document.getElementById('idsearchForm');
  if (!form) return;

  form.onsubmit = function() {
    var input = document.querySelector('.idsearchTerm').value.trim();
    var searchUrl;

    if (/^\d+$/.test(input)) {
        searchUrl = '/' + encodeURIComponent(input);
    } else if (/^((\d+|end)(-(\d+|end))?\s*)+(open|solved|yes|no)?$/.test(input.toLowerCase())) {
        let parts = input.split(/\s+/).filter(Boolean);
        searchUrl = '/range/' + parts.map(encodeURIComponent).join('/');
    } else {
        alert("Enter either a single integer or a space-separated list of numbers/ranges...");
        return false;
    }
    window.location.href = searchUrl;
    return false;
  };
});
</script>

<script>
  window.CURRENT_USERNAME = "";
</script>


<script>
document.addEventListener("click", async (ev) => {
  const btn = ev.target.closest(".reaction-btn");
  if (!btn) return;
  const you = window.CURRENT_USERNAME || "";
  const bar = btn.closest(".reaction-bar");
  const postId = bar?.dataset.postId;
  const rtype = btn.dataset.type;
  const reactUrl = bar?.dataset.reactUrl; 
  if (!postId || !rtype || !reactUrl) return;

  try {
    const res = await fetch(reactUrl, {
      method: "POST",
      credentials: "same-origin",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({type: rtype})
    });
    const data = await res.json();
    if (!data.ok) {
      alert(data.error || "Could not update reaction.");
      return;
    }
    const summary = data.summary;
    
    bar.querySelectorAll(".reaction-btn").forEach(b => {
      const t = b.dataset.type;
      const countSpan = bar.querySelector(`.reaction-count[data-type="${t}"]`);
      if (countSpan && summary[t]) {
        countSpan.textContent = summary[t].count;
    const desc = b.dataset.desc || "";
    const usersTitle = summary[t].users_title || "No one yet.";
    b.title = `${desc}\n\n${usersTitle}`;
      }
        const iReacted = you && (summary[t].users_title || "").includes(you);
  b.classList.toggle("active", !!iReacted);
  b.setAttribute("aria-pressed", iReacted ? "true" : "false");
    });
  } catch (e) {
    console.error(e);
    alert("Only registered users with 5+ posts can react.");
  }
});
</script>

<script>
document.addEventListener("DOMContentLoaded", function () {
  document.body.addEventListener("click", function (e) {
    const link = e.target.closest(".problem-reaction-link");
    if (!link) return;

    e.preventDefault();

    const row = link.closest(".problem-reaction-row");
    if (!row) return;

    const form = row.querySelector(".problem-reaction-form");
    if (!form) return;

    const formData = new FormData(form);

    fetch(form.action, {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest"
      }
    })
      .then(resp => resp.json())
      .then(data => {
        if (!data.ok) {
          console.error(data.error || "Problem reaction update failed");
          return;
        }

        const summary = data.summary;

        // Update users text for each reaction type
        for (const [type, info] of Object.entries(summary)) {
          const r = document.querySelector(
            `.problem-reaction-row[data-reaction-type="${type}"]`
          );
          if (!r) continue;

          const usersCell = r.querySelector(".problem-reaction-users");
          if (usersCell) {
            usersCell.textContent = info.users_title || "None yet";
          }
        }
        link.classList.toggle("active");
        if (link.classList.contains("active")) {
          link.textContent = "(no)";
        } else {
          link.textContent = "(yes)";
        }
      })
      .catch(err => {
        console.error("Problem reaction AJAX error", err);
      });
  });
});
</script>






</head>

<body>

<div class="topnav">

  <div class="left">
    <div class="logo">
      <a class="dual-aware" href="/"><img src="/static/EPLogo.png" alt="Logo" height="50"></a>
    </div>
    <div class="links dual-aware desktop-nav">
      <a href="/forum">Forum</a>
      <a href="/dm">Inbox</a> 
      <a href="/favourites">Favourites</a>
      <a href="/tags">Tags</a> 
      <div class="dropdown">
        <a href="javascript:void(0)" class="dropbtn">More</a>
        <div class="dropdown-content">
          <a href="/faq">FAQ</a>
          <a href="/prizes">Prizes</a>
          <a href="/lists">Problem Lists</a>
          <a href="/definitions">Definitions</a>
          <a href="/links">Links</a>
        </div>
      </div> 
    </div>
    <div class="mobile-nav">
    
        <a class="forumlink" href="/forum">Forum</a>
    <div class="dropdown">
      <button class="dropbtn" id="mobileMenuButton">Menu</button>
      <div class="dropdown-content">
        <a href="/dm">Inbox</a> 
        <a href="/favourites">Favourites</a>
        <a href="/tags">Tags</a>  
        <a href="/faq">FAQ</a>
        <a href="/prizes">Prizes</a>
        <a href="/lists">Problem Lists</a>
        <a href="/definitions">Definitions</a>
        <a href="/links">Links</a>
      </div>
     </div>
    </div>
  </div>

  <div class = "middle">
    <div class="button-container" style="max-width: 50%;">
      <form id="idsearchForm">
        <input required type="text" name="query" class="idsearchTerm" placeholder="# (or range #-#)" title="Enter either a single integer or a space-separated list of numbers/ranges, optionally ending with 'open' or 'solved'.">
        <button type="submit" class="searchButton">Go</button>
      </form>
    </div>
    <div class="button-container" style="max-width: 50%;">
      <form id="searchForm">
        <input required type="text" name="query" class="searchTerm" placeholder="Search" title="Search all problems.">
        <button type="submit" class="searchButton">Go</button>
      </form>
    </div>
  </div>

  <div class="right">
    <a href="#" id="dualViewLink" class="split_all">Dual View</a>
    <a href="/random_solved" class="split_solved dual-aware">Random Solved</a>
    <a href="/random_open" class="split_open dual-aware">Random Open</a>
  </div>

</div>

<div id="notifications-slot"></div>

<script>
(function () {
  const params = new URLSearchParams(window.location.search);
  if (params.get("embed")) return;

  fetch("/forum/notifications/fragment", {cache: "no-store"})
    .then(r => r.text())
    .then(html => {
      document.getElementById("notifications-slot").innerHTML = html;
    })
    .catch(() => {});
})();
</script>


<div class="container">
  <div class="problem-box">
    <div class="problem-text">  
      <div id="content" style="white-space: pre-line;">
      Let $\epsilon&#62;0$ and $k\geq 2$. Is it true that, for all sufficiently large $n$, there is a sequence of $k$ consecutive integers in $\{1,\ldots,n\}$ all of which are $n^\epsilon$-smooth?
      </div>
    </div>
  <div class="problem-additional-text" style="white-space: pre-line;"> 
  
  Erd\H{o}s and Graham state that this is open even for $k=2$ and 'the answer should be affirmative but the problem seems very hard'. These remarks are puzzling, since in 1976 Eggleton and Selfridge \cite{EgSe76} had already shown that, for any $\epsilon&gt;0$, there exist infinitely many sets of $5$ consecutive integers $\{n,\ldots,n+4\}$, each of which is $n^\epsilon$-smooth. <br><br>The problem is trivially true as written (simply taking $\{1,\ldots,k\}$ and $n&gt;k^{1/\epsilon}$). There are (at least) two possible variants which are non-trivial, and it is not clear which Erd\H{o}s and Graham meant. Let $P$ be the sequence of $k$ consecutive integers sought for. Some potential strengthenings which make this non-trivial are:<br>{UL}<br>{LI}Each $m\in P$ must be $m^\epsilon$-smooth. If this is the problem then the answer is yes, which follows from a result of Balog and Wooley \cite{BaWo98}: for any $\epsilon&gt;0$ and $k\geq 2$ there exist infinitely many $m$ such that $m+1,\ldots,m+k$ are all $m^\epsilon$-smooth.{/LI}<br>{LI}Each $m\in P$ must be in $[n/2,n]$ (say). In this case a positive answer also follows directly from the result of Balog and Wooley \cite{BaWo98} for infinitely many $n$. Proving this is true for all large $n$ does not follow immediately from \cite{BaWo98}, but can be deduced using a similar construction, as <a href="<br>https://drive.google.com/file/d/1MxgrA2haXKv_NKSa7sqUI2hZYyZ5JmfP/view?usp=drivesdk" rel="nofollow noopener noreferrer ugc" target="_blank">shown</a> by SkyYang. <br><br>A stronger result can be deduced from the main result of Bober, Fretwell, Martin, and Wooley \cite{BFMW20}; as discussed in the comments, this shows that, for any $\epsilon&gt;0$ and $k\geq 2$, there exists a constant $c&lt;1$ (depending on $k$ and $\epsilon$) such that, for all large $n$, there exists a sequence of $k$ consecutive integers, all $n^\epsilon$-smooth, in $[n-n^{c},n]$.{/LI}<br>{/UL}<br><br>See also <a href="/370" rel="nofollow noopener noreferrer ugc" target="_blank">[370]</a> and <a href="/928" rel="nofollow noopener noreferrer ugc" target="_blank">[928]</a>.
  
  </div>
  
  <div class="problem-additional-text" style="white-space: pre-line;"> 
  <h3>References</h3>
  
  [BFMW20] Bober, J. W. and Fretwell, D. and Martin, G. and Wooley, T. D., <i>Smooth values of polynomials</i>. J. Aust. Math. Soc. (2020), 245--261.
  
  [BaWo98] Balog, Antal and Wooley, Trevor D., <i>On strings of consecutive integers with no large prime factors</i>. J. Austral. Math. Soc. Ser. A (1998), 266-276.
  
  [EgSe76] Eggleton, R. B. and Selfridge, J. L., <i>Consecutive integers with no large prime factors</i>. J. Austral. Math. Soc. Ser. A (1976), 1--11.
  
  </div>
                                        
  <div class="problem-additional-text" style="text-align:center; padding: 10px;">
  <a href="/369">Back to the problem</a>
  </div>

</div>                

    





<!-- Previewing forum posts -->
<!-- Previewing forum posts -->
<script>
document.addEventListener("DOMContentLoaded", function () {
  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, m => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;"
    })[m]);
  }

  function normalizeHref(href) {
    href = href.trim();
    if (!/^https?:\/\//i.test(href) && !href.startsWith("/")) {
      href = "https://" + href;
    }

    return href;
  }

  let mathJaxQueue = Promise.resolve();

  function clearMathJax(element) {
    if (window.MathJax && MathJax.typesetClear) {
      MathJax.typesetClear([element]);
    }
  }

  function typesetMath(element) {
    if (!window.MathJax) return;

    if (MathJax.typesetPromise) {
      mathJaxQueue = mathJaxQueue
        .then(() => {
          if (MathJax.startup && MathJax.startup.promise) {
            return MathJax.startup.promise;
          }
        })
        .then(() => MathJax.typesetPromise([element]))
        .catch(err => {
          console.error("MathJax typeset failed:", err);
        });

      return;
    }

    if (MathJax.Hub) {
      MathJax.Hub.Queue(["Typeset", MathJax.Hub, element]);
    }
  }

  function renderPreview(textarea, preview, label) {
    let raw = textarea.value;
    const anchors = [];
    let idx = 0;

    raw = raw.replace(
      /<a\s+href=("(?:[^"]*)"|'(?:[^']*)')\s*>([\s\S]*?)<\/a>/gi,
      (match, qHref, labelText) => {
        const href = qHref.slice(1, -1);
        const token = `__A_TAG_${idx++}__`;

        anchors.push({
          token,
          href: normalizeHref(href),
          label: labelText
        });

        return token;
      }
    );

    let safe = escapeHtml(raw);

    anchors.forEach(a => {
      const html = `<a href="${escapeHtml(a.href)}">${escapeHtml(a.label)}</a>`;
      safe = safe.replace(a.token, html);
    });

    safe = safe.replace(/\{PROBLEM=(.+?)\}/g, (_, p1) =>
      `<a href="/${escapeHtml(p1)}">[${escapeHtml(p1)}]</a>`
    );

    safe = safe.replace(/\n/g, "<br>");
    clearMathJax(preview);

    if (!safe.trim()) {
      preview.innerHTML = "";
      preview.classList.add("hidden");
      label.classList.add("hidden");
      return;
    }

    preview.innerHTML = safe;
    preview.classList.remove("hidden");
    label.classList.remove("hidden");

    typesetMath(preview);
  }

  document.querySelectorAll("form textarea").forEach(textarea => {
    const form = textarea.closest("form");
    const preview = form && form.querySelector(".post-preview");
    const label = form && form.querySelector(".preview-label");

    if (preview && label) {
      textarea.addEventListener("input", () => renderPreview(textarea, preview, label));
      renderPreview(textarea, preview, label);
    }
  });
});
</script>

<!-- To handle the search bar -->
<script>
document.addEventListener('DOMContentLoaded', function () {
    function setFilterLink(linkId, newFilter) {
        const link = document.getElementById(linkId);
        if (!link) return;
        const pathParts = window.location.pathname.split("/");
        // Expect: /<section>/<entry> or /<section>/<entry>/<filter>
        if (pathParts.length >= 3) {
            const section = pathParts[1];
            const entry = pathParts[2];
            // Construct base: /tags/additive, /sources_bib/BL09, etc.
            const baseUrl = "/" + section + "/" + entry;
            link.href = baseUrl + "/" + newFilter;
        }
    }
    setFilterLink("solvedLink", "solved");
    setFilterLink("openLink", "open");
    setFilterLink("yesLink", "yes");
    setFilterLink("noLink", "no");
});
</script>

<!-- Handle the dual view link -->
<script>
document.addEventListener("DOMContentLoaded", function () {
  const dualLink = document.getElementById("dualViewLink");
  if (!dualLink) return;

  const isInDualView = window.location.pathname.startsWith("/dual");
  dualLink.textContent = isInDualView ? "Exit Dual View" : "Dual View";
  dualLink.addEventListener("click", function (e) {
    e.preventDefault();

    if (isInDualView) {
      try {
        const leftIframe = document.getElementById("iframe-left");
        const src = leftIframe?.src || "/";
        let clean = src.replace(window.location.origin, "");
        clean = clean.replace(/[?&]embed=1/, "");

        window.location.href = clean;
      } catch (err) {
        window.location.href = "/";
      }
    } else {
      const currentPath = window.location.pathname + window.location.search;
      const rightPanelDefault = "/";
      const hash = `#left:${encodeURIComponent(currentPath)}&right:${encodeURIComponent(rightPanelDefault)}`;
      window.location.href = `/dual${hash}`;
    }
  });
});
</script>

<!-- Redirect links and searches when in dual view mode -->
<script>
document.addEventListener("DOMContentLoaded", function () {
  if (!window.location.pathname.startsWith("/dual")) return;

  function getTargetPanel() {
    const selected = document.querySelector('input[name="targetPanel"]:checked');
    return selected ? selected.value : "left";
  }

  function loadInPanel(panel, path) {
    if (!path) return;
    const iframe = document.getElementById(`iframe-${panel}`);
    if (!iframe) return;
    const url = path.includes("?") ? path + "&embed=1" : path + "?embed=1";
    iframe.src = url;
    const inputBox = document.querySelector(`#panel-${panel} input`);
    if (inputBox) inputBox.value = path;
    console.log(`Loaded "${url}" into panel "${panel}"`);
  }
  
  document.querySelectorAll(".dual-aware a[href^='/'], a.dual-aware[href^='/']").forEach(link => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const path = this.getAttribute("href");
      loadInPanel(getTargetPanel(), path);
    });
  });

  const idForm = document.getElementById("idsearchForm");
  if (idForm) {
    idForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const input = idForm.querySelector(".idsearchTerm").value.trim();
      if (!input) return;

      let path = null;

      if (/^\d+$/.test(input)) {
        path = "/go_to/" + encodeURIComponent(input);
      } else if (/^((\d+|end)(-(\d+|end))?\s*)+(open|solved|yes|no)?$/i.test(input)) {
        const parts = input.split(/\s+/).filter(Boolean);
        path = "/range/" + parts.map(encodeURIComponent).join("/");
      } else {
        alert("Invalid input format.");
        return;
      }

      loadInPanel(getTargetPanel(), path);
    });
  }

  const searchForm = document.getElementById("searchForm");
  if (searchForm) {
    searchForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const input = searchForm.querySelector(".searchTerm").value.trim();
      if (!input) return;

      const path = "/search/" + encodeURIComponent(input);
      loadInPanel(getTargetPanel(), path);
    });
  }
});
</script>

<!-- Different menu on mobile -->

<script>
document.addEventListener("DOMContentLoaded", function () {
  const button = document.getElementById("mobileMenuButton");
  const dropdown = document.getElementById("mobileDropdown");

  if (button && dropdown) {
    button.addEventListener("click", function () {
      dropdown.classList.toggle("show");
    });

    document.addEventListener("click", function (e) {
      if (!button.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove("show");
      }
    });
  }
});
</script>

<!-- For expanding threads -->

<script>
document.addEventListener('click', (e) => {
  const link = e.target.closest('#toggle-posts');
  if (!link) return;
  e.preventDefault(); 

  const box = document.getElementById('more-posts');
  const isHidden = box.classList.toggle('hidden');
  const expanded = !isHidden;

  link.setAttribute('aria-expanded', expanded ? 'true' : 'false');
  box.setAttribute('aria-hidden', expanded ? 'false' : 'true');

  link.textContent = expanded
    ? 'Show only the top five comments'
    : `Show ${link.dataset.remaining} more comments`;
});
</script>


<script>
document.addEventListener('click', (e) => {
  const link = e.target.closest('.toggle-replies');
  if (!link) return;
  e.preventDefault();

  const pid = link.dataset.postId;
  const box = document.getElementById(`more-replies-${pid}`);
  if (!box) return;

  const isHidden = box.classList.toggle('hidden');
  const expanded = !isHidden;

  link.setAttribute('aria-expanded', expanded ? 'true' : 'false');
  box.setAttribute('aria-hidden', expanded ? 'false' : 'true');

  link.textContent = expanded
    ? 'Hide replies'
    : `Show ${link.dataset.remaining} more replies`;
});
</script>


<script>
document.addEventListener("click", async function (event) {
    const button = event.target.closest(".problem-status-option");
    if (!button) return;

    const widget = button.closest(".problem-status-widget");
    if (!widget) return;

    if (widget.dataset.canEdit !== "1") return;

    const status = button.dataset.status;
    const url = widget.dataset.setUrl;

    widget.classList.add("is-saving");

    const buttons = widget.querySelectorAll(".problem-status-option");
    buttons.forEach(btn => btn.disabled = true);

    try {
        const response = await fetch(url, {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json",
                "X-Requested-With": "fetch"
            },
            body: JSON.stringify({ status: status })
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok || !data.ok) {
            throw new Error(data.error || "Could not update problem status.");
        }

        widget.dataset.currentStatus = data.status;

        buttons.forEach(btn => {
            const active = btn.dataset.status === data.status;
            btn.classList.toggle("is-active", active);
            btn.setAttribute("aria-checked", active ? "true" : "false");
        });

        const label = widget.querySelector(".js-problem-status-label");
        const description = widget.querySelector(".js-problem-status-description");

        if (label) label.textContent = data.label || button.dataset.label;
        if (description) description.textContent = data.description || button.dataset.description;
          widget.style.setProperty("--status-progress", button.dataset.progress);

    } catch (err) {
        alert(err.message || "Could not update problem status.");
    } finally {
        widget.classList.remove("is-saving");

        if (widget.dataset.canEdit === "1") {
            buttons.forEach(btn => btn.disabled = false);
        }
    }
});
</script>
  
<script defer src="https://static.cloudflareinsights.com/beacon.min.js/v4513226cdae34746b4dedf0b4dfa099e1781791509496" integrity="sha512-ZE9pZaUXND66v380QUtch/5sE9tPFh2zg45pR2PB0CVkCtOREv2AJKkSidISWkysEuQ0EH8faUU5du78bx87UQ==" data-cf-beacon='{"version":"2024.11.0","token":"b8844510a8d24cfb9a8920cc04221446","r":1,"server_timing":{"name":{"cfCacheStatus":true,"cfEdge":true,"cfExtPri":true,"cfL4":true,"cfOrigin":true,"cfSpeedBrain":true},"location_startswith":null}}' crossorigin="anonymous"></script>
</body>
</html>
```

## Hosted theorem — plby (https://github.com/plby/lean-proofs/blob/main/src/v4.29.1/ErdosProblems/Erdos369.lean)

```lean
theorem erdos_problem_369 (ε : ℝ) (hε : 0 < ε) (k : ℕ) (hk : 2 ≤ k) :
    ∃ N₀ : ℕ, ∀ N : ℕ, N₀ ≤ N →
      ∃ a : ℕ, N / 2 ≤ a - (k - 1) ∧ a ≤ N ∧ k ≤ a ∧
        ∀ j : ℕ, j < k → (Nat.largestPrimeFactor (a - j) : ℝ) ≤ ((a - j : ℕ) : ℝ) ^ ε
```

## Hosted theorem — jayyhk (https://github.com/Jayyhk/erdos-lean/blob/main/problems/369/Erdos369.lean)

```lean
/-- The largest prime factor of a natural number n.
    Returns 0 if n ≤ 1 (no prime factors). -/
def Nat.largestPrimeFactor (n : ℕ) : ℕ :=
  if n ≤ 1 then 0 else n.primeFactors.sup id

lemma Nat.largestPrimeFactor_le (n : ℕ) : Nat.largestPrimeFactor n ≤ n := by
  unfold Nat.largestPrimeFactor; rcases n with ( _ | _ | n ) <;> simp +arith +decide;
  exact fun p pp dp => Nat.le_of_dvd ( Nat.succ_pos _ ) dp

lemma Nat.le_largestPrimeFactor {n p : ℕ} (hp : p ∈ n.primeFactors) :
    p ≤ Nat.largestPrimeFactor n := by
  unfold Nat.largestPrimeFactor;
  split_ifs <;> simp_all +decide;
  · interval_cases n <;> aesop;
  · exact Finset.le_sup ( f := id ) ( by aesop )

/-- The product ∏_{X₀ < p ≤ X₁} (1 - 1/p) can be made arbitrarily small. -/
lemma exists_prime_interval_small_euler_product (θ : ℝ) (hθ : 0 < θ) (X₀ : ℕ) :
    ∃ X₁ : ℕ, X₀ < X₁ ∧
      ∏ p ∈ (Finset.Icc (X₀ + 1) X₁).filter Nat.Prime, (1 - (1 : ℝ) / p) < θ := by
  have h_prod_zero : Filter.Tendsto (fun X₁ : ℕ => ∏ p ∈ Finset.filter Nat.Prime (Finset.Icc (X₀ + 1) X₁), (1 - 1 / (p : ℝ))) Filter.atTop (nhds 0) := by
    have h_sum_diverges : Filter.Tendsto (fun X₁ => ∑ p ∈ Finset.filter Nat.Prime (Finset.Icc (X₀ + 1) X₁), (1 / (p : ℝ))) Filter.atTop Filter.atTop := by
      have h_sum_diverges : Filter.Tendsto (fun X₁ : ℕ => ∑ p ∈ Finset.filter Nat.Prime (Finset.range X₁), (1 / (p : ℝ))) Filter.atTop Filter.atTop := by
        convert Nat.Primes.not_summable_one_div using 1;
        constructor <;> intro h <;> rw [ Filter.tendsto_atTop_atTop ] at *;
        · convert Nat.Primes.not_summable_one_div using 1;
        · intro b
          obtain ⟨i, hi⟩ : ∃ i : Finset ℕ, (∀ p ∈ i, Nat.Prime p) ∧ (∑ p ∈ i, (1 / (p : ℝ))) > b := by
            contrapose! h;
            refine' summable_of_sum_le _ _;
            exacts [ b, fun _ => by positivity, fun u => by simpa using h ( u.image Subtype.val ) fun p hp => by obtain ⟨ q, hq, rfl ⟩ := Finset.mem_image.mp hp; exact q.2 ];
          exact ⟨ i.sup id + 1, fun n hn => hi.2.le.trans <| Finset.sum_le_sum_of_subset_of_nonneg ( fun p hp => Finset.mem_filter.mpr ⟨ Finset.mem_range.mpr <| lt_of_le_of_lt ( Finset.le_sup ( f := id ) hp ) hn, hi.1 p hp ⟩ ) fun _ _ _ => by positivity ⟩;
      have h_eq : ∀ X₁ : ℕ, X₁ ≥ X₀ + 1 → ∑ p ∈ Finset.filter Nat.Prime (Finset.Icc (X₀ + 1) X₁), (1 / (p : ℝ)) = (∑ p ∈ Finset.filter Nat.Prime (Finset.range (X₁ + 1)), (1 / (p : ℝ))) - (∑ p
```

```lean
/-- Erdős Problem 369, the intended (non-trivial) interpretation settled by SkyYang:
for every `ε > 0` and `k ≥ 2`, for all sufficiently large `N` there are `k` consecutive
integers `a-(k-1), …, a` lying in `[N/2, N]`, all of which are `Nᵉ`-smooth
(every prime factor `≤ Nᵉ`). -/
theorem erdos_369 (ε : ℝ) (hε : 0 < ε) (k : ℕ) (hk : 2 ≤ k) :
    ∃ N₀ : ℕ, ∀ N : ℕ, N₀ ≤ N →
      ∃ a : ℕ, N / 2 ≤ a - (k - 1) ∧ a ≤ N ∧ k ≤ a ∧
        ∀ j : ℕ, j < k → (Nat.largestPrimeFactor (a - j) : ℝ) ≤ (N : ℝ) ^ ε
```

## Drafting rules
- Derive the statement from the problem text; the hosted theorems are a shape prior. Record EVERY divergence between your statement and each hosted theorem in draft.json divergence_notes.
- Category must match upstream state; verbatim docstring; erdos_<n> naming; one @[category], AMS tags; sorry body.
