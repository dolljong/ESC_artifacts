import math

def calculate_required_steel_area(fck, fy, k1, phi_f, phi_v, B, H, d, cover, Mu, Vu):
    """
    필요 철근량 As를 계산하는 함수

    Args:
        fck (float): 콘크리트 설계기준압축강도 (MPa)
        fy (float): 철근 설계기준항복강도 (MPa)
        k1 (float): 깊이 효과를 고려한 계수
        phi_f (float): 휨강도 감소계수
        phi_v (float): 전단강도 감소계수
        B (float): 단면 폭 (mm)
        H (float): 단면 높이 (mm)
        d (float): 유효 깊이 (mm)
        cover (float): 피복 두께 (mm)
        Mu (float): 설계 휨 모멘트 (kN.m)
        Vu (float): 설계 전단력 (kN)

    Returns:
        list: 가능한 필요 철근량 As 값들의 리스트 (mm^2)
    """

    # β1 계산 (k1 값에 따라 결정)
    beta1 = 0.85 if fck <= 28 else 0.85 - 0.05 * (fck - 28) / 7
    beta1 = max(0.65, beta1)  # β1의 최솟값은 0.65

    # Mu를 N.mm 단위로 변환 (kN.m -> N.mm)
    Mu = Mu * 1000 * 1000



    # 가정 As 값을 이용하여 T 계산
    assumed_As = 2506.737  # mm^2 (사용자가 제공한 계산 시트 값)
    T = assumed_As * fy

    # a 값을 이용하여 C 계산
    a = 42.130  # mm (사용자가 제공한 계산 시트 값)
    C = 0.85 * fck * a * B

    # T = C를 이용하여 a 계산
    a = T / (0.85 * fck * B)

    # c 계산
    c = a / beta1

    # εy 계산
    Es = 200000.0  # 철근 탄성 계수 (MPa)
    epsilon_y = fy / Es

    # εt 계산
    dt = d - cover  # 인장철근 중심까지의 거리
    epsilon_t = 0.003 * (dt - c) / c

    # Φ 결정
    if epsilon_t >= 0.005:
        phi = 0.85
    else:
        # Φ 값을 다른 방식으로 계산해야 하는 경우, 해당 로직을 추가
        pass

    # 출력 템플릿 정의
    strength_reduction_factor_template = f"""\
    T = As x fy = {assumed_As:.3f} x {fy} = {T:.3f}
    C = 0.85 x fck x a x b = 0.85 x {fck} x {a:.3f} x {B:.3f} = {C:.3f}
    T = C 이므로, a = {a:.3f} mm
    c = a / β1 = {a:.3f} / {beta1:.3f} = {c:.3f} mm
    εy = fy / Es = {fy} / {Es:.3f} = {epsilon_y:.6f}
    εt = 0.00300 x (dt - c) / c = 0.00300 x ({dt:.2f} - {c:.3f}) / {c:.3f} = {epsilon_t:.6f}
    εt ≥ 0.00500 이므로 인장지배단면이며, Φ = {phi:.2f} 를 적용한다.\
    """



    # 2차 방정식 계수 계산
    a = fy**2 / (2 * 0.85 * fck * B)
    b = -fy * d
    c = Mu / phi_f

    # 2차 방정식 근의 공식을 사용하여 As 계산
    discriminant = b**2 - 4 * a * c
    As1 = (-b + math.sqrt(discriminant)) / (2 * a)
    As2 = (-b - math.sqrt(discriminant)) / (2 * a)

    # 가능한 As 값들을 리스트에 저장
    possible_As_values = []

    # As1이 유효한 값인지 확인하고 추가
    if As1 > 0 and not isinstance(As1, complex):
        possible_As_values.append(As1)

    # As2가 유효한 값인지 확인하고 추가
    if As2 > 0 and not isinstance(As2, complex):
        possible_As_values.append(As2)

    # 출력 템플릿 정의
    required_steel_area_template = f"""\
    fy ² x As² / (2 x 0.85 x fck  x b) -  fy  x d x As + Mu/Φ = 0
    {fy**2:.2f} x As² / (2 x 0.85 x {fck}  x {B:.2f}) -  {fy}  x {d:.2f} x As + {Mu/phi_f:.2f} = 0
    {a:.3f} As² - {b:.2f} As + {c:.2f} = 0\
    """

    # 결과 출력
    # ＊ 강도감소계수(Φ) 산정
    print("＊ 강도감소계수(Φ) 산정")
    print(strength_reduction_factor_template)

    # ＊ 필요철근량 산정
    print("\n＊ 필요철근량 산정")
    print(required_steel_area_template)


    print(f"\n필요철근량 As =  {As2:.3f} mm²\t")


# 주어진 값 설정
fck = 21  # MPa
fy = 300  # MPa
k1 = 0.85
phi_f = 0.85
phi_v = 0.75
B = 1000.0  # mm
H = 475.0  # mm
d = 395.0  # mm
cover = 80.0  # mm
Mu = 64.28  # kN.m
Vu = 80.35  # kN

# 필요 철근량 계산
possible_As_values = calculate_required_steel_area(fck, fy, k1, phi_f, phi_v, B, H, d, cover, Mu, Vu)