"""Exercise the demo UI without writing to the local database.

Run after starting Django:
    python -m pip install --target .ui-test-deps playwright
    python scripts/check_app_ui.py
Uses the installed Edge browser. API writes are fulfilled by test fixtures.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / ".ui-test-deps"))
from playwright.sync_api import expect, sync_playwright

OUTPUT = ROOT / "artifacts" / "ui"
OUTPUT.mkdir(parents=True, exist_ok=True)
URL = "http://127.0.0.1:8000/app/"

users = [
    dict(id=1, public_handle="piano-note", age_group="30s", country_code="KR", gender="female", bio="매일 조금씩 연주하는 중이에요."),
    dict(id=2, public_handle="another-view", age_group="20s", country_code="JP", gender="male", bio="사진과 음악을 좋아해요."),
    dict(id=3, public_handle="slow-listener", age_group="50s", country_code="KR", gender="female", bio="다른 시선으로 감상해요."),
]
works = [
    dict(id=11, title="한 달 연습한 피아노 연주", summary="조용한 저녁에 어울리는 곡을 연주했어요.", creator_intent="차분하고 편안한 느낌을 전하고 싶어요. 중간에 템포가 빨라지지는 않나요?", creator=users[0], media_type="audio", assets=[]),
    dict(id=12, title="낯선 도시의 오후", summary="여행 중 찍은 사진입니다.", creator_intent="낯선 거리에서도 따뜻함이 느껴질까요?", creator=users[1], media_type="image", assets=[]),
    dict(id=13, title="수영 자유형 자세 연습", summary="호흡과 자세를 연습하고 있어요.", creator_intent="호흡할 때 몸이 많이 흔들리는지 궁금해요.", creator=users[0], media_type="video", assets=[]),
]
comments = [
    dict(id=i + 1, work=11, author=users[1 if i % 2 == 0 else 2], body=("감정이 잘 전달되고 여운이 좋아요." if i % 2 == 0 else "중간 박자가 불명확하고 호흡이 부족합니다."), focus_area="sound", status="active")
    for i in range(12)
]
failed_comment = False
writes = []

def serve_api(route):
    global failed_comment
    request = route.request
    resource = request.url.split("/api/")[1].split("/")[0]
    if request.method == "POST":
        payload = request.post_data_json
        writes.append((resource, payload))
        if resource == "comments":
            if failed_comment:
                route.fulfill(status=503, json={"detail": "Simulated failure"})
                return
            item = dict(id=999, work=payload["work_id"], author=users[0], body=payload["body"], focus_area=payload["focus_area"], status="active")
            comments.append(item)
        elif resource == "works":
            item = dict(payload, id=99, creator=users[0])
            works.insert(0, item)
        elif resource == "reports":
            item = dict(payload, id=1)
        else:
            raise AssertionError("Unexpected write")
        route.fulfill(status=201, json=item)
    else:
        route.fulfill(json={"results": {"users": users, "works": works, "comments": comments, "reports": []}[resource], "next": None})

def no_overflow(page):
    assert page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "Page overflows horizontally"
    assert page.locator("#screen").evaluate("(el) => el.scrollWidth <= el.clientWidth + 1"), "App content overflows"

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    real = browser.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    errors = []
    real.on("pageerror", lambda error: errors.append(str(error)))
    real.goto(URL)
    expect(real.locator("#feedCount")).to_contain_text("개의 작품")
    no_overflow(real)
    real.screenshot(path=str(OUTPUT / "feed-mobile.png"))
    if real.locator(".work-row").count():
        real.locator(".work-row").first.click()
        expect(real.locator("#detailHeading")).to_be_visible()
        real.locator('[data-detail-tab="insights"]').click()
        expect(real.locator("#demographicInsights")).to_be_visible()
        real.screenshot(path=str(OUTPUT / "insights-mobile.png"))
    real.set_viewport_size({"width": 1280, "height": 900})
    real.locator('.tab[data-tab="feed"]').click()
    no_overflow(real)
    real.screenshot(path=str(OUTPUT / "feed-desktop.png"), scale="css")
    assert not errors, errors
    real.close()

    context = browser.new_context(viewport={"width": 390, "height": 844})
    context.route("**/api/**", serve_api)
    page = context.new_page()
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.goto(URL)
    expect(page.locator("#feedList .work-row")).to_have_count(3)
    page.locator("#feedSearch").fill("피아노")
    expect(page.locator("#feedList .work-row")).to_have_count(1)
    page.locator("#feedSearch").fill("찾을 수 없는 검색어")
    expect(page.get_by_text("찾는 작품이 아직 없어요.", exact=True)).to_be_visible()
    page.get_by_role("button", name="필터 초기화").click()
    page.locator('[data-media="image"]').click()
    expect(page.locator("#feedList .work-row")).to_have_count(1)
    page.locator('[data-media="all"]').click()
    page.locator('.tab[data-tab="library"]').click()
    expect(page.locator("#myWorkList .work-row")).to_have_count(2)
    page.locator('#myWorkList [data-work-id="11"]').click()
    expect(page.locator("#detailHeading")).to_have_text("한 달 연습한 피아노 연주")
    expect(page.locator("#commentList .comment")).to_have_count(6)
    page.locator("#moreComments").click()
    expect(page.locator("#commentList .comment")).to_have_count(12)
    page.locator('[data-detail-tab="insights"]').click()
    expect(page.locator("#groupInsights .sentiment-row")).to_have_count(2)
    assert page.locator(".insight-overview .sentiment-bars span").first.evaluate("(el) => getComputedStyle(el).backgroundColor") != "rgba(0, 0, 0, 0)", "Sentiment bars should have visible colors"
    for axis in ["country", "gender", "age"]:
        page.locator(f'[data-axis="{axis}"]').click()
        expect(page.locator(f'[data-axis="{axis}"]')).to_have_attribute("aria-pressed", "true")
    expect(page.locator("#groupInsights")).to_contain_text("50대")
    page.screenshot(path=str(OUTPUT / "insights-fixture.png"))
    page.locator('[data-detail-tab="feedback"]').click()
    page.locator("#commentBody").fill("좋은 연주입니다. 끝부분의 호흡을 더 들어보고 싶어요.")
    failed_comment = True
    page.locator('#commentForm button[type="submit"]').click()
    expect(page.locator("#commentNotice")).to_contain_text("저장하지 못했어요")
    expect(page.locator("#commentBody")).not_to_have_value("")
    failed_comment = False
    page.locator('#commentForm button[type="submit"]').click()
    expect(page.locator("#commentList")).to_contain_text("끝부분의 호흡")
    page.locator("#backToFeed").click()
    expect(page.locator('[data-section="library"]')).to_be_visible()
    page.locator("#composeWork").click()
    page.locator("#workTitle").fill("UI 검증용 글")
    page.locator("#workMedia").select_option("other")
    page.locator("#workIntent").fill("글의 의도가 잘 전해지는지 궁금해요.")
    page.locator('#workForm button[type="submit"]').click()
    expect(page.locator("#detailHeading")).to_have_text("UI 검증용 글")
    assert writes[-1][1]["assets"] == [], "Blank asset should not create a fake URL"
    page.go_back()
    expect(page.locator('[data-section="upload"]')).to_be_visible()
    page.locator('.tab[data-tab="profile"]').click()
    page.locator('[data-section="profile"] .demo-settings > summary').click()
    page.locator("#activeUser").select_option("3")
    page.locator('.tab[data-tab="library"]').click()
    expect(page.get_by_text("아직 등록한 작품이 없어요.", exact=True)).to_be_visible()
    for width in [320, 390, 430, 768, 1280]:
        page.set_viewport_size({"width": width, "height": 844})
        for section in ["feed", "library", "activity", "profile"]:
            page.locator(f'.tab[data-tab="{section}"]').click()
            no_overflow(page)
    assert not errors, errors
    browser.close()
    print(json.dumps({"result": "passed", "viewports": [320, 390, 430, 768, 1280], "mocked_writes": len(writes), "screenshots": str(OUTPUT)}, ensure_ascii=False))
