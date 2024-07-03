from patterns.bridge import Effect

class EffectManager:
    def apply_effect(self, effect: Effect, player):
        effect.apply(player)