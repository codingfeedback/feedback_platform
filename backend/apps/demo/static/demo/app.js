/* Presentation and navigation for the existing Django demo API. */
const icon = (name) => `<svg class="icon" aria-hidden="true"><use href="#i-${name}"/></svg>`;
const mediaIcon = (type) => ({ video: "video", audio: "audio", image: "gallery", illustration: "pen", other: "pen" }[type] || "gallery");
let toastTimeout;
const scrollPositions = {};
let detailOrigin = "feed";
let uploadOrigin = "feed";

function countryLabel(code) {
    return { KR: "한국", US: "미국", JP: "일본", FR: "프랑스", BR: "브라질", ID: "인도네시아", IN: "인도", DE: "독일", CA: "캐나다" }[code] || code || "미공개";
}

function safeMediaUrl(value) {
    try {
        const url = new URL(value);
        if (!["https:", "http:"].includes(url.protocol) || url.username || url.password) return "";
        if (["example.com", "www.example.com"].includes(url.hostname)) return "";
        return url.href;
    } catch { return ""; }
}

function notify(message, error = false) {
    clearTimeout(toastTimeout);
    const toast = $("#toast");
    toast.textContent = message;
    toast.classList.toggle("error", error);
    toast.hidden = false;
    toastTimeout = setTimeout(() => { toast.hidden = true; }, 4500);
}

function render() {
    renderSwitcher();
    renderStats();
    renderFeed();
    renderLibrary();
    renderDetail();
    renderActivity();
    renderProfile();
}

function renderSwitcher() {
    $("#activeUser").innerHTML = state.users.length ? state.users.map((user) =>
        `<option value="${user.id}" ${Number(state.activeUserId) === user.id ? "selected" : ""}>${escapeHtml(user.public_handle)} · ${ageLabel(user.age_group)}</option>`
    ).join("") : '<option value="">체험 사용자를 만들어주세요</option>';
}

function renderStats() {
    $("#stats").innerHTML = [["작품", state.works.length], ["사용자", state.users.length], ["피드백", state.comments.filter((c) => c.status === "active").length]]
        .map(([label, count]) => `<div class="stat"><b>${count}</b><span>${label}</span></div>`).join("");
}

function workCard(work) {
    const count = commentsFor(work.id).length;
    const mine = work.creator?.id === activeUser()?.id;
    const thumbnail = safeMediaUrl(work.assets?.[0]?.thumbnail_url);
    return `<button class="work-row" type="button" data-work-id="${work.id}">
        <span class="work-art ${escapeHtml(work.media_type)}">
            ${icon(mediaIcon(work.media_type))}<span>${escapeHtml(labels[work.media_type] || "작품")}</span>
            ${thumbnail ? `<img src="${escapeHtml(thumbnail)}" alt="" loading="lazy" referrerpolicy="no-referrer">` : ""}
        </span>
        <span class="work-copy">
            <span class="meta">${escapeHtml(work.creator?.public_handle || "창작자")}${mine ? " · 내 작품" : ""}</span>
            <b class="title">${escapeHtml(work.title)}</b>
            <span class="summary">${escapeHtml(work.creator_intent || work.summary || "어떤 느낌인지 함께 이야기해요.")}</span>
            <span class="work-meta"><span>${escapeHtml(labels[work.media_type] || "작품")}</span><span class="feedback-count">${icon("chat")} 피드백 ${count}</span>${!count ? '<span class="chip green">첫 의견을 기다려요</span>' : ""}</span>
        </span>
    </button>`;
}

function renderFeed() {
    const query = (state.search || "").toLocaleLowerCase();
    const works = state.works.filter((work) =>
        (state.media === "all" || work.media_type === state.media) &&
        [work.title, work.summary, work.creator_intent, work.creator?.public_handle].some((value) => String(value || "").toLocaleLowerCase().includes(query))
    );
    $("#feedCount").textContent = `${works.length}개의 작품`;
    $("#feedList").innerHTML = works.length ? works.map(workCard).join("") : `<div class="empty"><b>${state.works.length ? "찾는 작품이 아직 없어요." : "첫 번째 시도를 기다려요."}</b><p>${state.works.length ? "다른 검색어나 작품 종류로 찾아보세요." : "작품을 올리거나 데모 설정에서 샘플을 체험해보세요."}</p><button class="secondary" type="button" ${state.works.length ? 'data-action="clear-search"' : 'data-tab="profile"'}>${state.works.length ? "필터 초기화" : "데모 설정으로"}</button></div>`;
}

function renderLibrary() {
    const works = state.works.filter((work) => work.creator?.id === activeUser()?.id);
    $("#myWorkList").innerHTML = works.length ? works.map(workCard).join("") : '<div class="empty"><b>아직 등록한 작품이 없어요.</b><p>연습 중인 영상도, 미완성 글도 좋아요.<br>궁금한 점을 다른 시선에 물어보세요.</p><button class="secondary" type="button" data-tab="upload">첫 작품 올리기</button></div>';
}

function mediaPreview(work) {
    const url = safeMediaUrl(work.assets?.[0]?.asset_url);
    if (!url) return '<p class="media-unavailable">미디어가 연결되지 않은 작품이에요. 아래의 제작 의도와 의견을 살펴보세요.</p>';
    const safe = escapeHtml(url);
    const path = new URL(url).pathname.toLowerCase();
    let media = "";
    if (["image", "illustration"].includes(work.media_type) && /\.(png|jpe?g|webp|gif|avif)$/.test(path)) media = `<img src="${safe}" alt="${escapeHtml(work.title)}" referrerpolicy="no-referrer">`;
    if (work.media_type === "video" && /\.(mp4|webm|mov)$/.test(path)) media = `<video src="${safe}" controls preload="none" playsinline></video>`;
    if (work.media_type === "audio" && /\.(mp3|wav|m4a|ogg)$/.test(path)) media = `<audio src="${safe}" controls preload="none"></audio>`;
    return `${media ? `<div class="detail-media">${media}</div>` : ""}<a class="text-button" href="${safe}" target="_blank" rel="noopener noreferrer">작품 원본 열기 ${icon("arrow")}</a>`;
}

function renderDetail() {
    const work = selectedWork();
    if (!work) {
        $("#workDetail").innerHTML = '<div class="empty">작품을 찾을 수 없어요. 목록에서 다시 선택해주세요.</div>';
        $("#reportPanel").hidden = true;
        return;
    }
    $("#reportPanel").hidden = false;
    const comments = commentsFor(work.id);
    const mine = work.creator?.id === activeUser()?.id;
    $("#workDetail").innerHTML = `
        <div class="detail-top"><span class="chip blue">${escapeHtml(labels[work.media_type] || "작품")}</span><span class="muted">${comments.length}개의 피드백</span></div>
        <h1 class="detail-heading" id="detailHeading" tabindex="-1">${escapeHtml(work.title)}</h1>
        <div class="creator"><span class="avatar">${escapeHtml(initial(work.creator))}</span><span><b>${escapeHtml(work.creator?.public_handle || "창작자")}</b><span>${escapeHtml(personaMeta(work.creator))}</span></span></div>
        ${mediaPreview(work)}
        <div class="intent-card"><h3>이런 시선이 필요해요</h3><p>${escapeHtml(work.creator_intent || work.summary)}</p></div>
        <div class="detail-tabs" aria-label="작품 정보">
            <button class="detail-tab" data-detail-tab="feedback" type="button" aria-controls="detailFeedback">피드백 <span class="muted">${comments.length}</span></button>
            <button class="detail-tab" data-detail-tab="insights" type="button" aria-controls="detailInsights">반응 분석</button>
        </div>
        <div id="detailFeedback">
            <div class="feedback-intro"><p>좋았던 점과 바꿔볼 점을 나눠주세요.</p><button class="text-button" type="button" data-action="write-comment">의견 남기기 ${icon("pen")}</button></div>
            <div id="commentList" class="stack"></div>
            <button class="ghost more-button" id="moreComments" type="button">피드백 더 보기</button>
            <form class="form comment-form" id="commentForm">
                <div class="field"><label for="focusArea">어떤 부분을 이야기할까요?</label><select id="focusArea" name="focus_area"><option value="overall">전체적인 인상</option><option value="story">이야기·구성</option><option value="visual">이미지·표현</option><option value="sound">소리·연주</option><option value="editing">편집·흐름</option><option value="emotion">감정 전달</option><option value="other">기타</option></select></div>
                <div class="field"><label for="commentBody">나의 피드백</label><textarea id="commentBody" name="body" placeholder="어떤 부분이 좋았나요? 무엇을 바꿔보면 더 좋을까요?" maxlength="5000" required></textarea></div>
                <p class="field-help">${escapeHtml(activeUser()?.public_handle || "체험 사용자")} 닉네임으로 등록됩니다. 작품에 대한 구체적이고 정중한 의견을 남겨주세요.</p>
                <button class="primary" type="submit">피드백 보내기</button>
                <p class="notice" id="commentNotice" role="status"></p>
            </form>
        </div>
        <div id="detailInsights" hidden>${renderDemographicInsights(comments)}</div>
        ${mine ? '<details class="demo-settings"><summary>샘플 피드백으로 분석 체험하기 <span class="beta">DEMO</span></summary><p class="muted">테스트 사용자와 댓글을 생성합니다. 실제 평가 데이터가 아닙니다.</p><button class="secondary" id="seedMyWorkFeedback" type="button">내 작품에 100명 피드백 생성</button><p class="notice" id="batchFeedbackNotice" role="status"></p></details>' : ""}
    `;
    renderCommentList();
    setDetailTab(state.detailTab, false);
    $("#commentForm").addEventListener("submit", (event) => runForm(event, submitComment));
    $("#seedMyWorkFeedback")?.addEventListener("click", seedMyWorkFeedback);
}

function setDetailTab(tab, focus = true) {
    state.detailTab = tab;
    $$(".detail-tab").forEach((button) => {
        const selected = button.dataset.detailTab === tab;
        button.classList.toggle("active", selected);
        button.setAttribute("aria-pressed", String(selected));
    });
    if (!$("#detailFeedback")) return;
    $("#detailFeedback").hidden = tab !== "feedback";
    $("#detailInsights").hidden = tab !== "insights";
    if (focus) document.querySelector(`[data-detail-tab="${tab}"]`)?.focus({ preventScroll: true });
}

function renderComment(comment) {
    return `<article class="comment"><div class="row-top"><div class="creator"><span class="avatar">${escapeHtml(initial(comment.author))}</span><span><b>${escapeHtml(comment.author?.public_handle || "참여자")}</b><span>${escapeHtml(personaMeta(comment.author))}</span></span></div><span class="chip">${escapeHtml(labels[comment.focus_area] || "전체")}</span></div><p>${escapeHtml(comment.body)}</p></article>`;
}

function renderCommentList() {
    const comments = commentsFor(selectedWork()?.id);
    $("#commentList").innerHTML = comments.length ? comments.slice(0, state.commentLimit).map(renderComment).join("") : '<div class="empty"><b>아직 도착한 피드백이 없어요.</b><p>작품을 보고 느낀 첫인상을 들려주세요.</p></div>';
    $("#moreComments").hidden = comments.length <= state.commentLimit;
    $("#moreComments").textContent = `피드백 더 보기 · ${Math.max(0, comments.length - state.commentLimit)}개 남음`;
}

function sentimentBars(counts) {
    const values = ["positive", "neutral", "negative"];
    return `<div class="sentiment-bars" aria-hidden="true" style="--positive:${counts.positive}fr;--neutral:${counts.neutral}fr;--negative:${counts.negative}fr"><span></span><span></span><span></span></div><div class="sentiment-legend">${values.map((key) => `<span>${sentimentLabel(key)} ${sentimentPercent(counts, key)}%</span>`).join("")}</div>`;
}

function renderDemographicInsights(comments) {
    if (!comments.length) return '<section id="demographicInsights"><div class="empty"><b>의견이 쌓이면 차이가 보여요.</b><p>연령대·국가·성별에 따른 반응과 대표 코멘트를 여기에 모아드릴게요.</p></div></section>';
    const counts = sentimentCounts(comments);
    const participants = new Set(comments.map((comment) => comment.author?.id).filter(Boolean)).size;
    return `<section class="insight-grid" id="demographicInsights">
        <div class="insight-overview"><h3>평가 성향 요약</h3><div class="insight-stat"><b>${participants}명</b><span>참여 · 피드백 ${comments.length}개</span></div>${sentimentBars(counts)}</div>
        <div><h2>누구에게 어떻게 전해졌을까요?</h2><div class="axis-tabs" aria-label="분석 기준">${[["age", "연령대"], ["country", "국가"], ["gender", "성별"]].map(([axis, label]) => `<button type="button" data-axis="${axis}" aria-pressed="${axis === state.insightAxis}" class="${axis === state.insightAxis ? "active" : ""}">${label}</button>`).join("")}</div><div class="sentiment-grid" id="groupInsights">${groupInsights(comments)}</div></div>
        <p class="insight-summary">댓글 키워드로 추정한 긍정·중립·부정 비율이며, AI 평가나 직접 입력한 평점이 아닙니다. 비율의 기준은 댓글 수로, 같은 사람의 여러 의견이 포함될 수 있어요. 대표 코멘트는 가장 많은 평가 성향의 댓글 예시입니다. 전체 대중을 대표하는 결과는 아닙니다.</p>
    </section>`;
}

function groupInsights(comments) {
    const getters = { age: (c) => ageLabel(c.author?.age_group), country: (c) => countryLabel(c.author?.country_code), gender: (c) => genderLabel(c.author?.gender) };
    const groups = new Map();
    for (const comment of comments) {
        const label = getters[state.insightAxis](comment);
        if (!groups.has(label)) groups.set(label, []);
        groups.get(label).push(comment);
    }
    const entries = [...groups.entries()].sort((a, b) => state.insightAxis === "age" ? a[0].localeCompare(b[0], "ko", { numeric: true }) : b[1].length - a[1].length);
    return entries.map(([label, group]) => {
        const counts = sentimentCounts(group);
        const max = Math.max(...Object.values(counts));
        const leaders = Object.keys(counts).filter((key) => counts[key] === max);
        const people = new Set(group.map((c) => c.author?.id).filter(Boolean)).size;
        const verdict = leaders.length === 1 ? `${sentimentLabel(leaders[0])} 의견이 많아요` : "다양한 의견이 있어요";
        return `<article class="sentiment-row"><div class="sentiment-row-head"><b>${escapeHtml(label)}</b><span>${people}명 · ${group.length}개 의견</span></div><p class="muted" style="margin:6px 0 0">${verdict}${people < 5 ? " · 표본 적음" : ""}</p>${sentimentBars(counts)}<p class="quote"><b>대표 코멘트 · 의견 예시</b>${escapeHtml(representativeComment(group, leaders.length === 1 ? leaders[0] : null))}</p></article>`;
    }).join("");
}

function renderActivity() {
    const userId = activeUser()?.id;
    const mine = new Set(state.works.filter((w) => w.creator?.id === userId).map((w) => w.id));
    const comments = state.comments.filter((comment) => comment.status === "active" && (state.activityMode === "sent" ? comment.author?.id === userId : mine.has(comment.work) && comment.author?.id !== userId)).reverse();
    $("#activityList").innerHTML = comments.length ? comments.slice(0, 30).map((comment) => {
        const work = state.works.find((w) => w.id === comment.work);
        return `<article class="comment activity-card"><div class="creator"><span class="avatar">${escapeHtml(initial(comment.author))}</span><span><b>${escapeHtml(comment.author?.public_handle || "참여자")}</b><span>${escapeHtml(personaMeta(comment.author))}</span></span></div><p>${escapeHtml(comment.body)}</p><button class="text-button" type="button" data-work-id="${comment.work}">${escapeHtml(work?.title || "작품 보기")} ${icon("arrow")}</button></article>`;
    }).join("") + (comments.length > 30 ? '<p class="muted">최근 30개의 피드백이에요. 나머지 의견은 각 작품에서 볼 수 있어요.</p>' : "") : '<div class="empty"><b>아직 피드백이 없어요.</b><p>작품을 올리거나 다른 사람에게 첫 의견을 건네보세요.</p><button class="secondary" type="button" data-tab="feed">작품 둘러보기</button></div>';
}

function renderProfile() {
    const user = activeUser();
    const myWorks = state.works.filter((work) => work.creator?.id === user?.id);
    const myIds = new Set(myWorks.map((work) => work.id));
    const active = state.comments.filter((c) => c.status === "active");
    const received = active.filter((c) => myIds.has(c.work) && c.author?.id !== user?.id).length;
    const sent = active.filter((c) => c.author?.id === user?.id).length;
    $("#profilePanel").innerHTML = user ? `<div class="row-top"><div class="creator"><span class="avatar">${escapeHtml(initial(user))}</span><span><b>${escapeHtml(user.public_handle)}</b><span>${escapeHtml(personaMeta(user))}</span></span></div><p class="muted" style="margin:16px 0">${escapeHtml(user.bio || "함께 배우고 다듬는 중입니다.")}</p><div class="stats"><div class="stat"><b>${myWorks.length}</b><span>내 작품</span></div><div class="stat"><b>${received}</b><span>받은 피드백</span></div><div class="stat"><b>${sent}</b><span>남긴 피드백</span></div></div><button class="text-button" type="button" data-tab="library">내 작품 살펴보기 ${icon("arrow")}</button>` : '<p class="muted">아래 데모 체험 설정에서 사용자를 만들어 시작해보세요.</p>';
    $("#peopleList").innerHTML = state.users.map((person) => `<button class="person ${Number(state.activeUserId) === person.id ? "active" : ""}" type="button" data-user-id="${person.id}"><span class="avatar">${escapeHtml(initial(person))}</span><span><b>${escapeHtml(person.public_handle)}</b><span class="muted">${escapeHtml(personaMeta(person))}</span></span><span class="chip">${state.works.filter((w) => w.creator?.id === person.id).length}개</span></button>`).join("");
}

function switchSection(section, { historyMode = "push", restore = false, focus = true } = {}) {
    if (!$('[data-section="' + section + '"]')) return;
    if (section === "upload" && state.section !== "upload") uploadOrigin = state.section;
    scrollPositions[state.section] = $("#screen").scrollTop;
    state.section = section;
    $$(".section").forEach((element) => {
        const current = element.dataset.section === section;
        element.hidden = !current;
        element.classList.toggle("active", current);
    });
    $$(".tab").forEach((element) => {
        const current = element.dataset.tab === section || (section === "detail" && element.dataset.tab === detailOrigin);
        element.classList.toggle("active", current);
        if (current) element.setAttribute("aria-current", "page");
        else element.removeAttribute("aria-current");
    });
    $("#composeWork").hidden = !["feed", "library"].includes(section);
    $("#screen").scrollTop = restore ? scrollPositions[section] || 0 : 0;
    if (historyMode !== "none") {
        const hash = section === "detail" ? `#work/${state.selectedWorkId}` : `#${section}`;
        if (historyMode === "replace") history.replaceState(null, "", hash);
        else if (location.hash !== hash) history.pushState(null, "", hash);
    }
    if (focus) $("[data-section=" + section + "] h1")?.focus({ preventScroll: true });
}

function openWork(id, { historyMode = "push" } = {}) {
    if (state.section !== "detail") detailOrigin = ["feed", "library", "activity"].includes(state.section) ? state.section : "feed";
    state.selectedWorkId = Number(id);
    state.detailTab = "feedback";
    state.commentLimit = 6;
    renderDetail();
    switchSection("detail", { historyMode });
}

function restoreRoute() {
    const route = location.hash.slice(1);
    if (/^work\/\d+$/.test(route)) openWork(Number(route.split("/")[1]), { historyMode: "none" });
    else switchSection(["feed", "library", "activity", "profile", "upload"].includes(route) ? route : "feed", { historyMode: "none", restore: true, focus: false });
}

async function runForm(event, handler) {
    event.preventDefault();
    const form = event.currentTarget;
    const button = form.querySelector('button[type="submit"]');
    if (button.disabled) return;
    if (!activeUser() && form.id !== "userForm") {
        notify("나의 루프에서 체험 사용자를 먼저 선택해주세요.", true);
        return;
    }
    const notice = form.querySelector(".notice") || form.parentElement.querySelector(".notice");
    if (notice) { notice.textContent = ""; notice.classList.remove("error"); }
    const label = button.textContent;
    button.disabled = true;
    button.textContent = "보내는 중…";
    try { await handler(event); }
    catch (error) {
        if (notice?.isConnected) { notice.textContent = "저장하지 못했어요. 연결과 입력 내용을 확인하고 다시 시도해주세요."; notice.classList.add("error"); }
        notify("저장하지 못했어요. 작성한 내용을 확인하고 다시 시도해주세요.", true);
    } finally { button.disabled = false; button.textContent = label; }
}

document.addEventListener("error", (event) => {
    if (event.target.matches?.(".work-art img")) event.target.hidden = true;
}, true);

document.addEventListener("click", (event) => {
    const work = event.target.closest("[data-work-id]");
    if (work) { openWork(work.dataset.workId); return; }
    const user = event.target.closest("[data-user-id]");
    if (user) { state.activeUserId = Number(user.dataset.userId); render(); notify("체험 사용자를 전환했어요."); return; }
    const tab = event.target.closest("[data-tab]");
    if (tab) { switchSection(tab.dataset.tab); return; }
    const media = event.target.closest("[data-media]");
    if (media) {
        state.media = media.dataset.media;
        $$("[data-media]").forEach((button) => { button.classList.toggle("active", button === media); button.setAttribute("aria-pressed", String(button === media)); });
        renderFeed(); return;
    }
    const detail = event.target.closest("[data-detail-tab]");
    if (detail) { setDetailTab(detail.dataset.detailTab); return; }
    const axis = event.target.closest("[data-axis]");
    if (axis) {
        state.insightAxis = axis.dataset.axis;
        $$("[data-axis]").forEach((button) => { button.classList.toggle("active", button === axis); button.setAttribute("aria-pressed", String(button === axis)); });
        $("#groupInsights").innerHTML = groupInsights(commentsFor(selectedWork()?.id)); return;
    }
    const activity = event.target.closest("[data-activity]");
    if (activity) {
        state.activityMode = activity.dataset.activity;
        $$("[data-activity]").forEach((button) => { button.classList.toggle("active", button === activity); button.setAttribute("aria-pressed", String(button === activity)); });
        renderActivity(); return;
    }
    if (event.target.closest('[data-action="clear-search"]')) {
        state.search = ""; state.media = "all"; $("#feedSearch").value = "";
        $$("[data-media]").forEach((button) => { const active = button.dataset.media === "all"; button.classList.toggle("active", active); button.setAttribute("aria-pressed", String(active)); });
        renderFeed(); $("#feedSearch").focus(); return;
    }
    if (event.target.closest('[data-action="write-comment"]')) { $("#commentBody").focus(); return; }
    if (event.target.closest("#moreComments")) { state.commentLimit += 10; renderCommentList(); }
});

$("#feedSearch").addEventListener("input", (event) => { state.search = event.target.value.trim(); renderFeed(); });
$("#activeUser").addEventListener("change", (event) => { state.activeUserId = Number(event.target.value); render(); notify("체험 사용자를 전환했어요."); });
$("#composeWork").addEventListener("click", () => switchSection("upload"));
$("#backToFeed").addEventListener("click", () => switchSection(detailOrigin, { restore: true }));
$("#cancelUpload").addEventListener("click", () => switchSection(uploadOrigin, { restore: true }));
$("#refresh").addEventListener("click", async () => {
    const button = $("#refresh"); button.disabled = true;
    try { await loadAll(); notify("새로운 피드백까지 확인했어요."); }
    catch { notify("새로고침하지 못했어요. 잠시 후 다시 시도해주세요.", true); }
    finally { button.disabled = false; }
});
$("#seedCommunity").addEventListener("click", async () => {
    const button = $("#seedCommunity"); button.disabled = true; button.textContent = "샘플을 만드는 중…";
    try { await seedCommunity(false); notify("데모 작품을 추가했어요."); }
    catch { notify("샘플 생성 중 오류가 발생했어요. 새로고침 후 확인해주세요.", true); }
    finally { button.disabled = false; button.textContent = "커뮤니티 샘플 채우기"; }
});
$("#workForm").addEventListener("submit", (event) => runForm(event, submitWork));
$("#userForm").addEventListener("submit", (event) => runForm(event, submitUser));
$("#reportForm").addEventListener("submit", (event) => runForm(event, submitReport));
window.addEventListener("popstate", restoreRoute);
loadAll().then(restoreRoute).catch(() => {
    $("#feedList").innerHTML = '<div class="empty"><b>작품을 불러오지 못했어요.</b><p>연결을 확인하고 상단의 새로고침을 눌러주세요.</p></div>';
    notify("서버 연결을 확인해주세요.", true);
});
