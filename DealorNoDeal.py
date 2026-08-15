import random

def playDealorNoDeal():
    prize = [1000 , 2000 , 5000 , 10000 , 20000 , 50000 , 100000 , 200000 , 500000 , 1000000 , 1500000 , 2000000 , 2500000 ,
            3000000 , 4000000 , 5000000 , 10000000 , 15000000 , 20000000 , 25000000 , 50000000 , 100000000 , 200000000 , 
            250000000 , 500000000 , 1000000000]

    num_case = len(prize)

    print("=" * 50)
    print("CHÀO MỪNG ĐẾN VỚI: ĐI TÌM ẨN SỐ (DEAL OR NO DEAL)")
    print("=" * 50)
    print("Có 26 chiếc cặp với những giải thưởng khác nhau.")
    print("Bạn sẽ chọn một chiếc cặp để giữ lại, sau đó mở các chiếc còn lại để khám phá giá trị của chúng.")
    print("Sau khi mở một số lượng nhất định các chiếc cặp, ngân hàng sẽ đưa ra một lời đề nghị.")
    print("Bạn có thể chọn chấp nhận lời đề nghị (Deal) hoặc tiếp tục mở các chiếc cặp (No Deal).")

    # Initialize the game
    random.shuffle(prize)  # Shuffle the prize amounts
    cases = {i + 1: prize[i] for i in range(num_case)}
    active_cases = list(cases.keys())

    while True:
        try:
            player_case = int(input(f"Chọn chiếc vali của riêng bạn (từ 1 đến {num_case}): "))
            if player_case in active_cases:
                active_cases.remove(player_case)
                break
            print("Lựa chọn không hợp lệ hoặc vali đã được chọn. Vui lòng chọn lại!")
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ!")

    print(f"\n=> Bạn đã chọn giữ vali số **{player_case}**. Chúc bạn may mắn!\n")

    rounds = [
        (6, "Vòng 1: Mở 6 vali"),
        (5, "Vòng 2: Mở 5 vali"),
        (4, "Vòng 3: Mở 4 vali"),
        (3, "Vòng 4: Mở 3 vali"),
        (2, "Vòng 5: Mở 2 vali"),
        (1, "Vòng 6: Mở 1 vali"),
        (1, "Vòng 7: Mở 1 vali"),
        (1, "Vòng 8: Mở 1 vali"),
        (1, "Vòng cuối cùng: Mở 1 vali") ]

    game_over = False
    final_offer = 0

    for open_count, round_name in rounds:
        if len(active_cases) <= 1:
            break
            
        print(f"\n--- {round_name} ---")
        
        for _ in range(open_count):
            if len(active_cases) <= 1:
                break
            while True:
                try:
                    print(f"Các vali còn lại trên bàn: {sorted(active_cases)}")
                    case_to_open = int(input(f"Chọn một vali để mở (từ {min(active_cases)} đến {max(active_cases)}): "))
                    if case_to_open in active_cases:
                        active_cases.remove(case_to_open)
                        break
                    print("Lựa chọn không hợp lệ hoặc vali đã được mở. Vui lòng chọn lại!")
                except ValueError:
                    print("Vui lòng nhập một số nguyên hợp lệ!")

            val = cases[case_to_open]
            print(f"Giá trị bên trong vali số {case_to_open} là: {val:,} VND")

        remaining_prizes = [cases[case] for case in active_cases]
        average_prize = sum(remaining_prizes) / len(remaining_prizes)

        offer = int(average_prize * (0.4 + 0.05 * (9 - len(rounds))))
        print("\n" + "~" * 40)
        print(f"📞 ĐIỆN THOẠI TỪ NHÀ ĐẦU TƯ (BANKER):")
        print(f"Banker đề nghị mua lại vali của bạn với giá: **{offer:,} VND**")
        print("~" * 40)

        choice = input("Bạn có muốn chấp nhận lời đề nghị này không? (d/n): ").strip().lower()
        if choice == "d":
            print(f"\nBạn đã chấp nhận lời đề nghị của Ngân Hàng với giá: **{offer:,} VND**")
            print(f"Giá trị bên trong vali số {player_case} là: **{cases[player_case]:,} VND**")
            game_over = True
            final_offer = offer
            break
        else :
            print("Không chấp nhận !!")

    if not game_over:
        print("\n" + "=" * 50)
        print("VÒNG CUỐI CÙNG")
        print("=" * 50)
        last_remaining = active_cases[0]
        print(f"Trên bàn chỉ còn lại vali của bạn số {player_case} và vali số {last_remaining} .")

        swap_choice = input(f"Bạn có muốn đổi vali của mình với vali số {last_remaining} không? (y/n): ").strip().lower()
        final_case = last_remaining if swap_choice == 'y' else player_case
        other_case = player_case if swap_choice == 'y' else last_remaining

        print(f"\nBạn quyết định giữ vali số **{final_case}**.")
        print(f"Vali số {final_case} của bạn chứa: **{cases[final_case]:,} VND**")
        print(f"Vali còn lại (số {other_case}) chứa: **{cases[other_case]:,} VND**")
        print(f"\nCHÚC MỪNG BẠN ĐÃ HOÀN THÀNH TRÒ CHƠI!")

if __name__ == "__main__":
    playDealorNoDeal()
