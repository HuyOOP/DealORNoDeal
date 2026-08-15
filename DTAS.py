import random

def play_di_tim_an_so():
    # Danh sách các mức tiền thưởng tiêu chuẩn trong chương trình
    prizes = [
        1000, 5000, 10000, 20000, 50000, 
        100000, 200000, 500000, 1000000, 2000000, 
        5000000, 10000000, 25000000, 50000000, 100000000, 
        200000000, 500000000, 1000000000, 2000000000, 5000000000
    ]
    
    num_cases = len(prizes)
    
    # Xáo trộn ngẫu nhiên các giải thưởng vào các vali (từ 1 đến 20)
    random.shuffle(prizes)
    cases = {i + 1: prizes[i] for i in range(num_cases)}
    active_cases = list(cases.keys())
    
    print("=" * 50)
    print("CHÀO MỪNG ĐẾN VỚI: ĐI TÌM ẨN SỐ (DEAL OR NO DEAL)")
    print("=" * 50)
    
    # Bước 1: Người chơi chọn vali giữ lại cho mình
    while True:
        try:
            player_case = int(input(f"Chọn chiếc vali của riêng bạn (từ 1 đến {num_cases}): "))
            if player_case in active_cases:
                active_cases.remove(player_case)
                break
            print("Lựa chọn không hợp lệ hoặc vali đã được chọn. Vui lòng chọn lại!")
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ!")
            
    print(f"\n=> Bạn đã chọn giữ vali số **{player_case}**. Chúc bạn may mắn!\n")
    
    # Các mốc số lượng vali cần mở trước mỗi lần Banker ra giá
    rounds = [
        (3, "Vòng 1: Mở 3 vali"),
        (4, "Vòng 2: Mở 4 vali"),
        (4, "Vòng 3: Mở 4 vali"),
        (3, "Vòng 4: Mở 3 vali"),
        (2, "Vòng 5: Mở 2 vali"),
        (1, "Vòng 6: Mở 1 vali"),
        (1, "Vòng 7: Mở 1 vali"),
        (1, "Vòng 8: Mở 1 vali"),
        (1, "Vòng cuối: Mở 1 vali")
    ]
    
    game_over = False
    final_offer = 0

    for open_count, round_name in rounds:
        if len(active_cases) <= 1:
            break
            
        print(f"\n--- {round_name} ---")
        print(f"Các vali còn lại trên bàn: {sorted(active_cases)}")
        
        # Người chơi lần lượt mở vali trong vòng này
        for _ in range(open_count):
            if len(active_cases) <= 1:
                break
            while True:
                try:
                    chosen = int(input(f"Chọn 1 vali để mở ({sorted(active_cases)}): "))
                    if chosen in active_cases:
                        active_cases.remove(chosen)
                        break
                    print("Vali không hợp lệ hoặc đã được mở!")
                except ValueError:
                    print("Vui lòng nhập số hợp lệ!")
            
            # Tiết lộ giá trị bên trong vali vừa mở
            val = cases[chosen]
            print(f"-> Mở vali số **{chosen}** chứa giải thưởng: **{val:,} VND**")
        
        # Banker đưa ra lời đề nghị dựa trên trung bình các vali còn lại
        remaining_values = [cases[c] for c in active_cases] + [cases[player_case]]
        avg_value = sum(remaining_values) / len(remaining_values)
        # Công thức tính offer của Banker tăng dần theo tiến độ game
        offer = int(avg_value * (0.4 + 0.05 * (9 - len(rounds))))
        
        print("\n" + "~" * 40)
        print(f"📞 ĐIỆN THOẠI TỪ NHÀ ĐẦU TƯ (BANKER):")
        print(f"Banker đề nghị mua lại vali của bạn với giá: **{offer:,} VND**")
        print("~" * 40)
        
        choice = input("Bạn chọn **DEAL** (nhận tiền) hay **NO DEAL** (tiếp tục chơi)? (d/n): ").strip().lower()
        
        if choice == 'd':
            print(f"\nCHÚNG TA CÓ MỘT DEAL! Bạn đã ra về với **{offer:,} VND**.")
            print(f"Vali số {player_case} của bạn thực chất chứa: **{cases[player_case]:,} VND**.")
            game_over = True
            break
        else:
            print("=> NO DEAL! Trò chơi tiếp tục...")

    # Nếu chơi đến cuối cùng mà không bấm Deal
    if not game_over:
        print("\n" + "=" * 50)
        print("VÒNG CUỐI CÙNG")
        print("=" * 50)
        last_remaining = active_cases[0]
        print(f"Trên bàn chỉ còn lại vali của bạn (số {player_case}) và vali số {last_remaining}.")
        
        swap_choice = input(f"Bạn có muốn ĐỔI vali số {player_case} lấy vali số {last_remaining} không? (y/n): ").strip().lower()
        
        final_case = last_remaining if swap_choice == 'y' else player_case
        other_case = player_case if swap_choice == 'y' else last_remaining
        
        print(f"\nBạn quyết định giữ vali số **{final_case}**.")
        print(f"Vali số {final_case} của bạn chứa: **{cases[final_case]:,} VND**")
        print(f"Vali còn lại (số {other_case}) chứa: **{cases[other_case]:,} VND**")
        print(f"\nCHÚC MỪNG BẠN ĐÃ HOÀN THÀNH TRÒ CHƠI!")

if __name__ == "__main__":
    play_di_tim_an_so()