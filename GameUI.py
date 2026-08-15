import random
import tkinter as tk
from tkinter import messagebox
from tkinter import font

class DealOrNoDealGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Deal or No Deal")
        self.root.geometry("1200x720")
        self.root.config(bg="#1a1a2e")

        self.prizes = [1000 , 2000 , 5000 , 10000 , 20000 , 50000 , 100000 , 200000 , 500000 , 1000000 , 1500000 , 2000000 , 2500000 ,
            3000000 , 4000000 , 5000000 , 10000000 , 15000000 , 20000000 , 25000000 , 50000000 , 100000000 , 200000000 , 
            250000000 , 500000000 , 1000000000]

        random.shuffle(self.prizes)  # Shuffle the prize amounts
        self.cases = {i + 1: self.prizes[i] for i in range(26)}
        self.player_case = None
        self.active_cases = list(self.cases.keys())

        

        self.rounds = [
            (6, "Vòng 1: Mở 6 vali"),
            (5, "Vòng 2: Mở 5 vali"),
            (4, "Vòng 3: Mở 4 vali"),
            (3, "Vòng 4: Mở 3 vali"),
            (2, "Vòng 5: Mở 2 vali"),
            (1, "Vòng 6: Mở 1 vali"),
            (1, "Vòng 7: Mở 1 vali"),
            (1, "Vòng 8: Mở 1 vali"),
            (1, "Vòng cuối cùng: Mở 1 vali") ]

        self.current_round = 0
        self.opened_left_in_round = self.rounds[self.current_round][0]

        self.state = "Choose_Player_Case"  # Initial state: choosing the player's case

        self.create_widgets()

    def create_widgets(self):

        self.title_label = tk.Label(self.root, text="Deal or No Deal!", font=("Arial", 36), bg="#1a1a2e", fg="white")
        self.title_label.pack(pady=20)

        self.instruction_label = tk.Label(self.root, text="Choose for your case !!", font=("Arial", 18), bg="#1a1a2e", fg="white")
        self.instruction_label.pack(pady=10)

        self.case_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.case_frame.pack(pady=26)

        self.case_buttons = {}
        for i in range(1, 27):
            row = (i - 1) // 6
            col = (i - 1) % 6
            case_button = tk.Button(self.case_frame, text=f"Case {i}", font=("Arial", 14), width=10, height=2, bg="#162447", fg="white")
            case_button.grid(row=row, column=col, padx=10, pady=10)
            self.case_buttons[i] = case_button

        self.board_frame = tk.Frame(self.root, bg="#16213e", bd=2, relief=tk.GROOVE)
        self.board_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.Y)

        tk.Label(
            self.board_frame, text=" BẢNG GIẢI THƯỞNG ", 
            font=("Arial", 14, "bold"), fg="#f39c12", bg="#16213e"
        ).pack(pady=10)

        self.prize_labels = {}
        sorted_prizes = sorted(self.prizes, reverse=True)
        
        for idx, p in enumerate(sorted_prizes):
            row = (idx % 13) + 1  # 13 hàng mỗi cột
            col = idx // 13       # 2 cột (Cột 0 và Cột 1)
            lbl = tk.Label(
                self.board_frame, 
                text=f" {p:,} VND ", 
                font=("Arial", 11, "bold"), 
                fg="#2ecc71", 
                bg="#16213e",
                anchor="w"
            )
            lbl.pack(anchor="w", padx=15, pady=2)
            self.prize_labels[p] = lbl

        self.status_frame = tk.Frame(self.root, bg="#1a1a2e")
        self.status_frame.pack(pady=20)

        self.player_case_label = tk.Label(self.status_frame, text="Your Case: None", font=("Arial", 16), bg="#1a1a2e", fg="white")
        self.player_case_label.pack()

    def on_case_button_click(self, case_number):
        if self.state == "Choose_Player_Case":
            self.player_case = case_number
            self.active_cases.remove(case_number)
            self.case_buttons[case_number].config(state="disabled", bg="#2ecc71")
            self.player_case_label.config(text=f"Your Case: {self.player_case} (Đã giữ lại)")
            self.instruction_label.config(text="Now, open the other cases!")
            self.state = "Opening"
            self.instruction_label.config(text=f"Vòng 1 : Hãy open {self.opened_left_in_round} more case(s) in this round.")
            messagebox.showinfo("Case Selected", f"You have chosen Case {self.player_case} to keep. Good luck!")
        elif self.state == "Opening":
            if case_number not in self.active_cases:
                return  # Case already opened or selected
            
            self.active_cases.remove(case_number)
            opened_value = self.cases[case_number]
            if opened_value in self.prize_labels:
                self.prize_labels[opened_value].config(fg="#555555" , font=("Arial", 14, "overstrike"))  # Change color to black for opened prize
            self.case_buttons[case_number].config(state="disabled", bg="#e74c3c" , text=f"Case {case_number}\n${opened_value:,}")
            
            self.opened_left_in_round -= 1
            if self.opened_left_in_round > 0:
                    self.instruction_label.config(text=f"Cần mở thêm {self.opened_left_in_round} more case(s) in this round.")
            else:
                    if len(self.active_cases) <= 1:
                        self.end_game()
                    else:
                        self.trigger_bank_offer()

    def trigger_bank_offer(self):
        self.state = "Bank_Offer"
        remaining_prizes = [self.cases[case] for case in self.active_cases]
        average_prize = sum(remaining_prizes) / len(remaining_prizes)
         
        offer = int(average_prize * (0.4 + 0.05 * (9 - self.current_round)))
        self.instruction_label.config(text=f"📞 Đang có cuộc gọi từ Nhà đầu tư (Banker)...")           
        deal = messagebox.askyesno("Bank Offer", f"Nhà đầu tư (Banker) đưa ra lời đề nghị: {offer:,} VND.\nBạn có muốn chấp nhận lời đề nghị (Deal) không?")               
        if deal:
             messagebox.showinfo("Deal Accepted", f"Bạn đã chấp nhận lời đề nghị của Ngân Hàng với giá: {offer:,} VND\nGiá trị bên trong vali số {self.player_case} là: {self.cases[self.player_case]:,} VND")
             self.root.quit()
        else:
                messagebox.showinfo("Deal Rejected", "Không chấp nhận lời đề nghị của Ngân Hàng. Tiếp tục mở các vali còn lại.")
                self.current_round += 1
                if self.current_round < len(self.rounds):
                    self.opened_left_in_round = self.rounds[self.current_round][0]
                    self.state = "Opening"
                    self.instruction_label.config(text=f"Vòng {self.current_round + 1}: Hãy mở {self.opened_left_in_round} more case(s) in this round.")
                else:
                    self.end_game()

    def end_game(self):
        self.instruction_label.config(text="Game Over! Revealing your case...")
        last_case = self.active_cases[0] 
        player_value = self.cases[self.player_case]
        last_value = self.cases[last_case]

        swap_choice = messagebox.askyesno(
            "Vòng Cuối Cùng - Cơ hội đổi vali",
            f"Trên bàn chỉ còn lại 2 chiếc:\n"
            f"- Vali của bạn: Số {self.player_case}\n"
            f"- Vali còn lại trên bàn: Số {last_case}\n\n"
            f"Bạn có muốn ĐỔI vali số {self.player_case} lấy vali số {last_case} không?"
        )

        if swap_choice:
            final_case = last_case
            other_case = self.player_case
            swap_msg = f"Bạn đã đổi lấy vali số {last_case}."

        else:
            final_case = self.player_case
            other_case = last_case
            swap_msg = f"Bạn đã giữ lại vali số {self.player_case}."

        messagebox.showinfo(
            "Kết Quả Chung Cuộc",
            f"{swap_msg}\n\n"
            f"🎁 Vali bạn chọn chứa: **{self.cases[final_case]:,} VND**\n"
            f"📦 Vali còn lại chứa: **{self.cases[other_case]:,} VND**\n\n"
            f"Cảm ơn bạn đã tham gia chương trình !!"
        )
        self.root.quit()



if __name__ == "__main__":
    root = tk.Tk()
    game = DealOrNoDealGame(root)
    for case_number, button in game.case_buttons.items():
        button.config(command=lambda num=case_number: game.on_case_button_click(num))
    root.mainloop()

