import pygame

class InputSystem:
    def handle_events(self):
        """จัดการ Event ของ Pygame ส่งคืน False ถ้าต้องการปิดเกม"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def get_keys(self):
        """ดึงสถานะการกดปุ่มบนคีย์บอร์ดทั้งหมด"""
        return pygame.key.get_pressed()