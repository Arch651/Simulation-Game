from src.manager.game import GameManager


def main():
    # these will act as the reference point
    base_length_per_pixel: float = 6
    base_width_per_pixel: float = 5

    world_obj = GameManager(
        length_per_pixel=base_length_per_pixel, 
        width_per_pixel=base_width_per_pixel
    )

    world_obj.main_game_loop()


if __name__ == "__main__":
    main()


"""
(800,600) --> (2,2)
(800,600) --> (8.025,8)
(1920,1080) --> (19.48,15.8)
(1920,1080) --> (4.87,3.95)
(1970,1340) --> (5,5)
"""
