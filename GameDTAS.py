import random
import tkinter as tk
from tkinter import messagebox

class DealOrNoDealGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Đi Tìm Ân Số - Deal or No Deal")
        self.root.geometry("850x650")
        self.root.config(bg="#1a1a2e")

        # Danh sách 20 mức tiền thưởng
        self.prizes = [
            1000, 5000, 10000, 20000, 50000, 
            100000, 200000, 500000, 1000000, 2000000, 
            5000000, 10000000, 25000000, 50000000, 100000000, 
            200000000, 500000000, 1000000000, 2000000000, 5000000000
        ]
        
        random.shuffle(self.prizes)
        self.cases = {i + 1: self.prizes[i] for i in range(20)}
        
        self.player_case = None
        self.active_cases = list(range(1, 21))
        
        # Cấu hình các vòng mở vali (Số lượng vali cần mở mỗi vòng)
        self.round_steps = [3, 4, 4, 3, 2, 1, 1, 1, 1]
        self.current_round_idx = 0
        self.opens_left_in_round = self.round_steps[0]
        
        self.state = "CHOOSE_PLAYER_CASE" # Các trạng thái: CHOOSE_PLAYER_CASE, OPENING, OFFER
        
        self.create_widgets()

    def create_widgets(self):
        # Tiêu đề
        self.title_label = tk.Label(
            self.root, text="ĐI TÌM ẨN SỐ", 
            font=("Arial", 22, "bold"), fg="#f39c12", bg="#1a1a2e"
        )
        self.title_label.pack(pady=10)

        # Hướng dẫn
        self.instruction_label = tk.Label(
            self.root, text="Hãy chọn 1 chiếc vali giữ lại cho riêng bạn!", 
            font=("Arial", 14), fg="white", bg="#1a1a2e"
        )
        self.instruction_label.pack(pady=5)

        # Khung chứa các nút vali (4 hàng, 5 cột)
        self.cases_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.cases_frame.pack(pady=15)

        self.case_buttons = {}
        for i in range(1, 21):
            row = (i - 1) // 5
            col = (i - 1) % 5
            btn = tk.Button(
                self.cases_frame, text=str(i), font=("Arial", 14, "bold"),
                width=8, height=2, bg="#3498db", fg="white",
                command=lambda c=i: self.on_case_click(c)
            )
            btn.grid(row=row, column=col, padx=8, pady=8)
            self.case_buttons[i] = btn

        # Khung hiển thị thông tin vali của người chơi
        self.status_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.status_frame.pack(pady=10)
        
        self.player_case_label = tk.Label(
            self.status_frame, text="Vali của bạn: Chưa chọn", 
            font=("Arial", 12, "bold"), fg="#2ecc71", bg="#1a1a2e"
        )
        self.player_case_label.pack()

    def on_case_click(self, case_num):
        if self.state == "CHOOSE_PLAYER_CASE":
            self.player_case = case_num
            self.active_cases.remove(case_num)
            self.case_buttons[case_num].config(bg="#2ecc71", state="disabled")
            self.player_case_label.config(text=f"Vali của bạn: Số {case_num} (Đã giữ lại)")
            
            self.state = "OPENING"
            self.instruction_label.config(text=f"Vòng 1: Hãy chọn {self.opens_left_in_round} vali để mở.")
            messagebox.showinfo("Thông báo", f"Bạn đã chọn vali số {case_num}. Bây giờ hãy bắt đầu mở các vali khác!")

        elif self.state == "OPENING":
            if case_num not in self.active_cases:
                return
            
            # Mở vali
            self.active_cases.remove(case_num)
            val = self.cases[case_num]
            self.case_buttons[case_num].config(bg="#e74c3c", state="disabled", text=f"{case_num}\n({val:,})")
            
            self.opens_left_in_round -= 1
            
            if self.opens_left_in_round > 0:
                self.instruction_label.config(text=f"Cần mở thêm {self.opens_left_in_round} vali trong vòng này.")
            else:
                # Hết lượt mở trong vòng này -> Banker gọi điện
                if len(self.active_cases) <= 1:
                    self.end_game()
                else:
                    self.trigger_banker_offer()

    def trigger_banker_offer(self):
        self.state = "OFFER"
        
        # Tính toán đề nghị của Banker
        remaining_values = [self.cases[c] for c in self.active_cases] + [self.cases[self.player_case]]
        avg_value = sum(remaining_values) / len(remaining_values)
        offer = int(avg_value * (0.35 + 0.05 * (9 - self.current_round_idx)))
        
        self.instruction_label.config(text="📞 Đang có cuộc gọi từ Nhà đầu tư (Banker)...")
        
        # Hiển thị hộp thoại Deal / No Deal
        deal = messagebox.askyesno(
            "Đề nghị từ Banker", 
            f"📞 Cuộc gọi từ Banker:\n\nÔng ấy đề nghị mua lại vali của bạn với giá:\n{offer:,} VND\n\nBạn có muốn DEAL (Nhận tiền và dừng cuộc chơi) không?"
        )
        
        if deal:
            messagebox.showinfo(
                "Kết thúc", 
                f"CHÚNG TA CÓ MỘT DEAL!\nBạn ra về với số tiền: {offer:,} VND.\nVali số {player_case_real := self.player_case} của bạn chứa: {self.cases[self.player_case]:,} VND."
            )
            self.root.quit()
        else:
            # Chuyển sang vòng tiếp theo
            self.current_round_idx += 1
            if self.current_round_idx < len(self.round_steps):
                self.opens_left_in_round = self.round_steps[self.current_round_idx]
                self.state = "OPENING"
                self.instruction_label.config(text=f"Vòng {self.current_round_idx + 1}: Hãy chọn {self.opens_left_in_round} vali để mở.")
            else:
                self.end_game()

    def end_game(self):
        self.instruction_label.config(text="TRÒ CHƠI KẾT THÚC!")
        last_remaining = self.active_cases[0]
        player_val = self.cases[self.player_case]
        last_val = self.cases[last_remaining]
        
        messagebox.showinfo(
            "Vòng Cuối Cùng",
            f"Trên bàn chỉ còn lại 2 vali:\n- Vali của bạn (Số {self.player_case}): {player_val:,} VND\n- Vali còn lại (Số {last_remaining}): {last_val:,} VND\n\nCảm ơn bạn đã tham gia Đi Tìm Ấn Số!"
        )
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = DealOrNoDealGame(root)
    root.mainloop()