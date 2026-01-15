import streamlit as st
import pandas as pd
import datetime
import uuid
import time

st.set_page_config(page_title="밥상매치 MVP", layout="wide", page_icon="🍚")

if 'requests' not in st.session_state: st.session_state.requests = []
if 'bids' not in st.session_state: st.session_state.bids = []
if 'matches' not in st.session_state: st.session_state.matches = []

def generate_auto_bid(req_id, owner_name, vacancy_rate):
    offer = "20% 할인 + 특수부위" if vacancy_rate >= 0.7 else "음료수 1병 서비스"
    tag = "🔥파격제안" if vacancy_rate >= 0.7 else "일반제안"
    return {"bid_id": str(uuid.uuid4())[:8], "req_id": req_id, "owner_name": owner_name, "offer": offer, "tag": tag, "timestamp": datetime.datetime.now().strftime("%H:%M:%S")}

with st.sidebar:
    role = st.radio("역할 선택", ["👨‍👩‍👧‍👦 손님 (User)", "👨‍🍳 사장님 (Owner)", "📊 관리자 (Admin)"])
    if st.button("🔄 새로고침"): st.rerun()

if role == "👨‍👩‍👧‍👦 손님 (User)":
    st.title("👨‍👩‍👧‍👦 오늘 뭐 드시나요?")
    with st.container(border=True):
        c1, c2, c3 = st.columns(3)
        with c1: loc = st.text_input("위치", "광안리")
        with c2: pp = st.number_input("인원", 1, 10, 4)
        with c3: menu = st.selectbox("메뉴", ["회", "고기"])
        if st.button("📢 호출하기", type="primary", use_container_width=True):
            st.session_state.requests.append({"id": str(uuid.uuid4())[:8], "location": loc, "people": pp, "menu": menu, "status": "입찰대기", "time": datetime.datetime.now().strftime("%H:%M:%S")})
            st.toast("전송 완료!"); time.sleep(1); st.rerun()
    
    if st.session_state.requests:
        req = st.session_state.requests[-1]
        st.write(f"내 요청 상태: {req['status']}")
        my_bids = [b for b in st.session_state.bids if b['req_id'] == req['id']]
        for b in my_bids:
            if st.button(f"수락: {b['owner_name']} ({b['offer']})", key=b['bid_id']):
                st.session_state.matches.append(b)
                req['status'] = "매칭완료"
                st.balloons(); st.toast("매칭 성공!"); st.rerun()

elif role == "👨‍🍳 사장님 (Owner)":
    st.title("👨‍🍳 사장님 알림판")
    vacancy = st.slider("빈자리 비율", 0.0, 1.0, 0.8)
    reqs = [r for r in st.session_state.requests if r['status'] in ["입찰대기"]]
    for r in reqs:
        st.write(f"🔔 {r['menu']} {r['people']}명 ({r['location']})")
        if st.button("⚡ 제안 보내기", key=f"b_{r['id']}"):
            st.session_state.bids.append(generate_auto_bid(r['id'], "내 식당", vacancy))
            r['status'] = "제안도착"
            st.toast("발송 완료!"); st.rerun()

elif role == "📊 관리자 (Admin)":
    st.write("매칭 내역:", st.session_state.matches)
