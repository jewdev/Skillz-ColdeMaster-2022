from penguin_game import *


def do_turn(game):
    my_icebergs_count = len(game.get_my_icebergs())
    for iceberg in game.get_my_icebergs():
        if iceberg.can_upgrade() and iceberg.upgrade_cost + 10 < iceberg.penguin_amount:
            iceberg.upgrade()
        else:
            if my_icebergs_count < 3:
                for neutral_iceberg in game.get_neutral_icebergs():
                    if not already_sent(game, neutral_iceberg):
                        if iceberg.can_send_penguins(neutral_iceberg, neutral_iceberg.penguin_amount + 1):
                            iceberg.send_penguins(
                                neutral_iceberg, neutral_iceberg.penguin_amount + 1)
            else:
                for enemyIceberg in game.get_enemy_icebergs():
                    send_enemy(iceberg, enemyIceberg)
                for enemy_group in game.get_enemy_penguin_groups():
                    if enemy_group.destination in game.get_my_icebergs():
                        counter_attack(enemy_group.destination, enemy_group.source,
                                       enemy_group.penguin_amount, game.get_my_icebergs())


def already_sent(game, dest):
    for group in game.get_my_penguin_groups():
        if group.destination == dest:
            return True
    return False


def send_enemy(source, dest):
    amount = dest.penguins_per_turn * \
        source.get_turns_till_arrival(dest) + dest.penguin_amount + 1
    if source.can_send_penguins(dest, amount):
        source.send_penguins(dest, amount)
        return True
    return False


def counter_attack(my_iceberg, source, enemy_amount, icebergs):
    penguin_amount = my_iceberg.penguin_amount
    if enemy_amount < my_iceberg.penguin_amount:
        neighbor = find_closest(icebergs, my_iceberg)
        if my_iceberg.can_send_penguins(source, my_iceberg.penguin_amount - 1):
            my_iceberg.send_penguins(source, my_iceberg.penguin_amount - 1)
        if neighbor.can_send_penguins(my_iceberg, enemy_amount-penguin_amount):
            neighbor.send_penguins(my_iceberg, enemy_amount-penguin_amount)
    else:
        neighbor = find_closest(icebergs, my_iceberg)
        my_amount = source.get_turns_till_arrival(
            my_iceberg) * my_iceberg.penguins_per_turn + my_iceberg.penguin_amount
        if neighbor.can_send_penguins(my_iceberg, enemy_amount-my_amount + 1):
            neighbor.send_penguins(my_iceberg, enemy_amount-my_amount + 1)


def find_closest(my_icebergs, iceberg):
    min = 100000000
    for my_iceberg in my_icebergs:
        if my_iceberg.get_turns_till_arrival(iceberg) < min and not iceberg == my_iceberg:
            min = my_iceberg.get_turns_till_arrival(iceberg)
            minIceberg = my_iceberg
    return minIceberg
