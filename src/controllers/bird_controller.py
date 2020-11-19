from src.entities.bird import Bird


class BirdController:
    def create_bird(self, position) -> Bird:
        return Bird(position)

    def flap(self, bird):
        bird.sprite.center_y += 2

    def fall(self):
        self.sprite.center_y -= 2
