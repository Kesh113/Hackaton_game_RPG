import random 
from colorama import init, Fore

init(autoreset=False)


PLAYERS_NUMBER = 10
MAX_THINGS_NUMBER = PLAYERS_NUMBER * 4
BASE_STATS_FOR_PERSON = random.randint(5, 15)
CRIT_DAMAGE = 2
PERSON_NAMES = random.sample([
  'Падаван', 'И.Маск', 'А.Лебедев', 'В.Путин', 'Трамп',
  'Бывалый', 'MrBeast', 'Зена', 'Мага', 'Гвидо ван Россум',
  'Б.Гейтс', 'М.Джексон', 'Д.Бычков', 'А.Руденко', 'Д.Есипов',
  'К.Вурст', 'А.Савиновский', 'Тор', 'Халк', 'Женщина-кошка'
], 10)


def crit_random_multiplier(crit_chance, crit_defence):
  final_crit_chance = (crit_chance - crit_defence) / 100
  no_crit_chance = 1 - final_crit_chance
  return random.choices([1, 2], [no_crit_chance, final_crit_chance])[0]


class Thing:
    def __init__(self, name, attack, health, protection, crit, crit_protection):
        self.name = name
        self.attack = attack
        self.health = health
        self.protection = protection
        self.crit = crit
        self.crit_protection = crit_protection

    def __str__(self):
        return f"Thing({self.name})"


def generate_things():
    things = []
    for thing in range(0, MAX_THINGS_NUMBER):
        thing = Thing(name=f"Thing {thing}",
                      attack=random.randint(1, 10),
                      health=random.randint(1, 10),
                      protection=random.randint(1, 10),
                      crit=random.randint(1, 10),
                      crit_protection=random.randint(1, 10))
        things.append(thing)
    return things


class Person:
    def __init__(self, name=None):
        self.name = name
        self.hp = BASE_STATS_FOR_PERSON
        self.base_attack = BASE_STATS_FOR_PERSON
        self.base_def = BASE_STATS_FOR_PERSON
        self.base_crit = BASE_STATS_FOR_PERSON
        self.base_crit_protection = BASE_STATS_FOR_PERSON

    def set_things(self, things):
        for thing in things:
            self.hp += thing.health
            self.base_attack += thing.attack
            self.base_def += thing.protection
            self.base_crit += thing.crit
            self.base_crit_protection += thing.crit_protection

    def loss_hp(self, hit, enemy_crit):
        self.hp -= hit * crit_random_multiplier(enemy_crit, self.base_crit_protection) * self.base_def / 100


class Paladin(Person):
  def __init__(self, name=None):
    super().__init__(name)
    self.hp *= 2
    self.base_def *= 2

  def __str__(self):
    return f'{self.name} - Паладин'


class Warrior(Person):
  def __init__(self, name=None):
    super().__init__(name)
    self.base_attack *= 2

  def __str__(self):
    return f'{self.name} - Воин'


class Archer(Person):
  def __init__(self, name=None):
    super().__init__(name)
    self.base_crit *= 2

  def __str__(self):
    return f'{self.name} - Лучник'

def generate_persons():
    things = generate_things()
    players = []
    for i in range(PLAYERS_NUMBER):
        player_things = [things.pop() for _ in range(random.randint(1, 5))]
        player = random.choice([Paladin(), Warrior(), Archer()])
        player.name = PERSON_NAMES.pop()
        player.set_things(player_things)
        players.append(player)
    return players


if __name__ == '__main__':
    persons = generate_persons()
    while True:
        attacker = random.choice(persons)
        defenders = persons.copy()
        defenders.remove(attacker)
        defender = random.choice(defenders)
        attacker_hp = attacker.hp
        defender_hp = defender.hp
        while True:
            proxy_d = defender.hp
            proxy_a = attacker.hp
            defender.loss_hp(attacker.base_attack, defender.base_crit)
            print(Fore.BLUE + f'Атакующий: {attacker} нанес {round(proxy_d - defender.hp, 2)} урона защитнику {defender} ')
            if defender.hp <= 0:
                persons.remove(defender)
                winner = 'a'
                print(Fore.RED + f'Защитник {defender} погиб')
                break
            attacker.loss_hp(defender.base_attack, attacker.base_crit)
            print(Fore.BLUE + f'Защитник: {defender} нанес {round(proxy_a - attacker.hp, 2)} урона атакубщему {attacker} ')
            if attacker.hp <= 0:
                winner = 'd'
                print(Fore.RED + f'Атакующий {attacker} погиб')
                persons.remove(attacker)
                break
        if winner == 'a':
            print(Fore.GREEN + f'Победил {attacker} осталось {round(attacker.hp, 2)} здоровья')
            attacker.hp = attacker_hp
        else:
            print(Fore.GREEN + f'Победил {defender} осталось {round(defender.hp, 2)} здоровья')
            defender.hp = defender_hp
        if len(persons) == 1:
            print(Fore.YELLOW + f'Последний выживший {persons[0]}')
            break
