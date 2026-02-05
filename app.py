import streamlit as st
import pandas as pd

# --------------------------------------------------------------------------
# 0) 페이지/스타일 설정
# --------------------------------------------------------------------------
st.set_page_config(page_title="서울 장학금 추천", page_icon="🎓", layout="wide")

# 배경색: 모닝옐로우(#FFF9C4) 반영
st.markdown("""
<style>
  .stApp { background-color:#FFF9C4; } 
  .card {
    background:#fff; border:1px solid #e5e7eb; border-radius:12px;
    padding:14px; box-shadow:0 3px 10px rgba(0,0,0,.04); margin-bottom:8px;
  }
  .pill {
    display:inline-block; padding:3px 8px; border-radius:999px; font-size:13px;
    background:#fff7ed; color:#7c2d12; border:1px solid #fed7aa; margin-right:6px; margin-bottom:6px;
  }
  .btn-yellow {
    display:inline-block; text-decoration:none !important;
    background:#FFE999; color:#3a3a00 !important; font-weight:700;
    padding:8px 10px; border-radius:8px; border:1px solid #E6D77A;
    font-size:14px; line-height:1; white-space:nowrap;
  }
  .btn-row { display:flex; gap:8px; align-items:center; margin:8px 0 0; }
  .compact-hr { border:none; border-top:1px solid #e5e7eb; margin:10px 0; }
  .footer-inline { display:flex; gap:8px; align-items:center; flex-wrap:wrap; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------------------
# 1) 장학금 데이터 정의 (명칭 변경 반영)
# --------------------------------------------------------------------------
def create_scholarship_df():
    data = [
        # 대학원생 전용
        {'장학금명': 'AI서울테크연구지원사업', '구분': '대학원생', '학년 정보': '대학원 재학생',
         '전공 계열': 'AI/이공계', '필수 조건': '해당 없음', '경제상황 요건': '해당 없음',
         'url': 'https://www.hissf.or.kr/home/kor/M075356964/scholarship/info/view.do?idx=cb00d1a0008a85e71a41b8741facbffe0da50bb4e2a1672fcc14ff2318200bfa&idx3=cb00d1a0008a85e71a41b8741facbffe0da50bb4e2a1672fcc14ff2318200bfa&act=&tabPos3=C#'},

        # 대학생/대학원생 공통 (서울혁신스타트업지원사업)
        {'장학금명': '서울혁신스타트업지원사업', '구분': '대학생, 대학원생',
         '학년 정보': '대학 혹은 대학원 재학생', '전공 계열': '창업 예정자',
         '필수 조건': '해당 없음', '경제상황 요건': '해당 없음',
         'url': 'https://www.hissf.or.kr/home/kor/M338346211/scholarship/info/view.do?idx=cb00d1a0008a85e71a41b8741facbffe2a91d3ee98d60342f28473f4a1fdb3e4&idx3=cb00d1a0008a85e71a41b8741facbffe2a91d3ee98d60342f28473f4a1fdb3e4&act=&tabPos3=A'},

        # 대학생 전용
        {'장학금명': '서울인재대학장학금', '구분': '대학생',
         '학년 정보': '신입생(1학년), 재학생(2학년 이상)', '전공 계열': '전공무관',
         '필수 조건': '해당 없음',
         '경제상황 요건': '기초생활수급자/법정차상위계층, 학자금지원 4구간 이내',
         'url': 'https://www.hissf.or.kr/home/kor/M338346211/scholarship/info/view.do?idx=cb00d1a0008a85e71a41b8741facbffe4d70c2b189c2c79f9576c3797a0949b1&idx3=cb00d1a0008a85e71a41b8741facbffe4d70c2b189c2c79f9576c3797a0949b1&act=&tabPos3=A'},

        {'장학금명': '서울독립유공자후손장학금', '구분': '대학생',
         '학년 정보': '신입생(1학년), 재학생(2학년 이상)', '전공 계열': '전공무관',
         '필수 조건': '독립유공자 후손 (4~6대)', '경제상황 요건': '해당 없음',
         'url': 'https://www.hissf.or.kr/home/kor/M338346211/scholarship/info/view.do?idx=cb00d1a0008a85e71a41b8741facbffe3fc96574ebd8c66af64789274f5f686f&idx3=cb00d1a0008a85e71a41b8741facbffe3fc96574ebd8c66af64789274f5f686f&act=&tabPos3=A'},

        {'장학금명': '서울인재해외교환학생장학금', '구분': '대학생',
         '학년 정보': '재학생(2학년 이상)', '전공 계열': '전공무관',
         '필수 조건': '해외교환학생으로 선발된 자',
         '경제상황 요건': '기초생활수급자/법정차상위계층, 학자금지원 4구간 이내',
         'url': 'https://www.hissf.or.kr/home/kor/M338346211/scholarship/info/view.do?idx=cb00d1a0008a85e71a41b8741facbffe76bede247ad7fca503608770da735e0b&idx3=cb00d1a0008a85e71a41b8741facbffe76bede247ad7fca503608770da735e0b&act=&tabPos3=A'},

        {'장학금명': '청춘Start 장학금', '구분': '대학생',
         '학년 정보': '신입생(1학년)', '전공 계열': '전공무관', '필수 조건': '해당 없음',
         '경제상황 요건': '기초생활수급자/법정차상위계층, 아동복지시설 퇴소자',
         'url': 'https://www.hissf.or.kr/home/kor/M338346211/scholarship/info/view.do?idx=cb00d1a0008a85e71a41b8741facbffe71a547009cdc82b6a17d02db013fb623&idx3=cb00d1a0008a85e71a41b8741facbffe71a547009cdc82b6a17d02db013fb623&act=&tabPos3=A'},

        {'장학금명': '서울인재직업전문학교장학금', '구분': '대학생',
         '학년 정보': '직업전문학교 학생', '전공 계열': '전공무관', '필수 조건': '해당 없음',
         '경제상황 요건': '기초생활수급자/법정차상위계층',
         'url': 'https://www.hissf.or.kr/home/kor/M338346211/scholarship/info/view.do?idx=cb00d1a0008a85e71a41b8741facbffe33a0bf6dc445c148169c7d619bdff9fc&idx3=cb00d1a0008a85e71a41b8741facbffe33a0bf6dc445c148169c7d619bdff9fc&act=&tabPos3=A'},

        # 고등학생 전용
        {'장학금명': '서울미래고교장학금', '구분': '고등학생',
         '학년 정보': '고등학교 재학생', '전공 계열': '전공무관', '필수 조건': '해당 없음',
         '경제상황 요건': '기초생활수급자, 차상위계층, 북한이탈주민, 경제사각지대',
         'url': 'https://www.hissf.or.kr/home/kor/M125164715/scholarship/info/view.do?idx=cb00d1a0008a85e71a41b8741facbffe04b930aaf4ff976a1b2120a7ae0856f3&idx3=cb00d1a0008a85e71a41b8741facbffe04b930aaf4ff976a1b2120a7ae0856f3&act=&tabPos3=B'},

        {'장학금명': '서울미래예체능장학금', '구분': '고등학생',
         '학년 정보': '고등학교 재학생', '전공 계열': '예체능', '필수 조건': '예체능 특기자',
         '경제상황 요건': '기초생활수급자/법정차상위계층, 학교장 추천 받은 학생',
         'url': 'https://www.hissf.or.kr/home/kor/M125164715/scholarship/info/view.do?idx=cb00d1a0008a85e71a41b8741facbffe5af0e69807254d86d6a4697a439067f4&idx3=cb00d1a0008a85e71a41b8741facbffe5af0e69807254d86d6a4697a439067f4&act=&tabPos3=B'},

        {'장학금명': '서울미래꿈터장학금', '구분': '고등학생',
         '학년 정보': '비인가 대안교육기관 재학 청소년 또는 쉼터 거주 청소년', '전공 계열': '전공무관', '필수 조건': '학교장 추천',
         '경제상황 요건': '기초생활수급자/법정차상위계층, 학교장 추천',
         'url': 'https://www.hissf.or.kr/home/kor/M125164715/scholarship/info/view.do?idx=cb00d1a0008a85e71a41b8741facbffeb867cf7f5c7adc365326c976b22336f5&idx3=cb00d1a0008a85e71a41b8741facbffeb867cf7f5c7adc365326c976b22336f5&act=&tabPos3=B'}
    ]
    return pd.DataFrame(data)

# --------------------------------------------------------------------------
# 2) 결과 출력 UI
# --------------------------------------------------------------------------
def display_results(result_df):
    st.subheader("🏆 추천 장학금 결과")
    if result_df.empty:
        st.info("✅ 아쉽지만 현재 조건에 맞는 장학금이 없습니다.")
        return

    st.success(f"총 {len(result_df)}개의 장학금을 추천합니다!")

    BUTTON_LABEL = "해당 장학금 ‘사업 안내’로 이동 ↗"

    for _, row in result_df.iterrows():
        detail_url = row.get("url", "")
        if isinstance(detail_url, str) and detail_url.startswith(("http://", "https://")):
            btn_html = f'<a class="btn-yellow" href="{detail_url}" target="_blank">{BUTTON_LABEL}</a>'
        else:
            btn_html = '<span class="btn-yellow" style="opacity:.6;">사업 안내 링크 준비 중 🙏</span>'

        st.markdown(
            f"""
            <div class="card">
              <h4 style="margin:0 0 6px 0; font-size:18px;">🎓 {row['장학금명']}</h4>
              <div style="color:#6b7280; font-size:14px; margin-bottom:6px;">
                {row.get('구분','')} · {row.get('학년 정보','')}
              </div>
              <div style="margin-bottom:6px;">
                <span class="pill">전공: {row.get('전공 계열','-')}</span>
                <span class="pill">필수: {row.get('필수 조건','-')}</span>
                <span class="pill">경제: {row.get('경제상황 요건','-')}</span>
              </div>
              <div class="btn-row">{btn_html}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<hr class="compact-hr" />', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="footer-inline">
          <span style="font-size:13px; color:#374151;">🔗 더 많은 장학금 정보는 서울장학재단 공식 홈페이지/카카오 채널에서 확인하세요.</span>
          <a class="btn-yellow" href="https://www.hissf.or.kr/" target="_blank">서울장학재단 ‘홈페이지’로 이동 🏠</a>
          <a class="btn-yellow" href="https://pf.kakao.com/_xdxbTYxb" target="_blank">카카오톡 채널 추가하기 💬</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# --------------------------------------------------------------------------
# 3) 메인 로직
# --------------------------------------------------------------------------
def main():
    df = create_scholarship_df()

    st.title("✨ 나에게 맞는 서울 장학금 추천")
    st.write("간단한 질문에 답변하고, 나에게 딱 맞는 장학금을 찾아보세요!")

    main_type = st.selectbox("학생 구분을 선택해주세요.", ['--선택--', '대학원생', '대학생', '고등학생'])
    if main_type == '--선택--':
        return

    if main_type == '대학원생':
        # AI서울테크연구지원사업 및 서울혁신스타트업지원사업 노출
        display_results(df[df['구분'].str.contains('대학원생')])
        return

    if main_type == '대학생':
        status_options = ['--선택--', '신입생(1학년)', '재학생(2학년 이상)', '직업전문학교 학생']
        user_status = st.selectbox("학년 정보를 선택해주세요.", status_options)
        if user_status == '--선택--':
            return

        if user_status == '직업전문학교 학생':
            result_df = df[df['장학금명'] == '서울인재직업전문학교장학금']
            display_results(result_df)
            return

        if user_status == '신입생(1학년)':
            names = ['서울인재대학장학금', '청춘Start 장학금', '서울독립유공자후손장학금']
            result_df = df[df['장학금명'].isin(names)]
            display_results(result_df)
            return

        if user_status == '재학생(2학년 이상)':
            excluded = ['청춘Start 장학금', '서울인재직업전문학교장학금']
            result_df = df[(df['구분'].str.contains('대학생')) & (~df['장학금명'].isin(excluded))]
            display_results(result_df)
            return

    elif main_type == '고등학생':
        status_options = ['--선택--', '고등학교 재학생', '비인가 대안교육기관 재학 청소년 또는 쉼터 거주 청소년']
        user_status = st.selectbox("조금 더 상세한 신분을 선택해주세요.", status_options)
        if user_status == '--선택--': return
        if user_status == '비인가 대안교육기관 재학 청소년 또는 쉼터 거주 청소년':
            display_results(df[df['학년 정보'] == user_status]); return
        
        filtered_df = df[df['학년 정보'] == user_status]
        user_major = st.selectbox("전공 계열을 선택해주세요.", ['--선택--', '예체능', '기타'])
        if user_major == '--선택--': return

        eco_options = ['--선택--', '기초생활수급자 또는 법정차상위계층', '북한이탈주민', '경제적 지원 필요', '해당 없음']
        user_eco_choice = st.selectbox("경제적 상황을 선택해주세요.", eco_options)
        if user_eco_choice == '--선택--': return

        user_eco_conditions = []
        if user_eco_choice == eco_options[1]: user_eco_conditions = ['기초생활수급자', '차상위계층', '법정차상위계층']
        elif user_eco_choice == eco_options[2]: user_eco_conditions = ['북한이탈주민']
        elif user_eco_choice == eco_options[3]: user_eco_conditions = ['경제사각지대', '학교장 추천']

        final_recommendations = []
        for _, row in filtered_df.iterrows():
            if user_major == '예체능' and row['전공 계열'] != '예체능': continue
            if user_major == '기타' and row['전공 계열'] == '예체능': continue
            req_eco = row['경제상황 요건']
            if user_eco_choice == '해당 없음':
                if '해당 없음' in row['필수 조건'] and '해당 없음' in req_eco: final_recommendations.append(row)
            elif any(cond in req_eco for cond in user_eco_conditions): final_recommendations.append(row)
        display_results(pd.DataFrame(final_recommendations))

if __name__ == "__main__":
    main()