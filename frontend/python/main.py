import asyncio
import pygame as pg
from block import Bag, Hold, Stack, BLOCK_SIZE
from block import black, white, yellow, light_blue, purple, blue, orange, green, red
import time
from threading import Thread

pg.init()

KICK_TABLE = {
    "0 1" : [ [ 0, 0], [ 0,-1], [-1,-1], [ 2, 0], [ 2,-1], [ 0, 0] ],#0 -> 1
    "1 0" : [ [ 0, 0], [ 0, 1], [ 1, 1], [-2, 0], [-2, 1], [ 0, 0] ], #1 -> 0
    "1 2" : [ [ 0, 0], [ 0, 1], [ 1, 1], [-2, 0], [-2, 1], [ 0, 0] ], #1 -> 2
    "2 1" : [ [ 0, 0], [ 0,-1], [-1,-1], [ 2, 0], [ 2,-1], [ 0, 0] ],#2 -> 1
    "2 3": [ [ 0, 0], [ 0, 1], [-1, 1], [ 2, 0], [ 2, 1], [ 0, 0] ], #2 -> 3
    "3 2" : [ [ 0, 0], [ 0,-1], [ 1,-1], [-2, 0], [-2,-1], [ 0, 0] ], #3 -> 2
    "3 0" : [ [ 0, 0], [ 0,-1], [ 1,-1], [-2, 0], [-2,-1], [ 0, 0] ], #3 -> 0
    "0 3" : [ [ 0, 0], [ 0, 1], [-1, 1], [ 2, 0], [ 2, 1], [ 0, 0] ], #0 -> 3

    "0 2" : [ [ 0, 0], [-1, 0], [-1, 1], [-1,-1], [ 0, 1], [ 0,-1] ], #0 -> 2
    "2 0" : [ [ 0, 0], [ 1, 0], [ 1,-1], [ 1, 1], [ 0,-1], [ 0, 1] ], #2 -> 0
    "1 3" : [ [ 0, 0], [ 0, 1], [-2, 1], [-1, 1], [-2, 0], [-1, 0] ], #1 -> 3
    "3 1" : [ [ 0, 0], [ 0,-1], [-2,-1], [-1,-1], [-2, 0], [-1, 0] ] #3 -> 1
    }

I_KICK_TABLE = {
    "0 1" : [ [ 0, 0], [ 0, 1], [ 0, 2], [ 0,-1], [ 1,-1], [-2, 2], [ 0, 1] ], # 0 -> 1
    "1 0" : [ [ 0, 0], [ 0,-1], [ 0,-2], [ 0, 1], [ 2,-2], [-1, 1], [ 0,-1] ], # 1 -> 0
    "1 2" : [ [ 0, 0], [ 1, 0], [ 1,-1], [ 1, 2], [-1,-1], [ 2, 2], [ 1, 0] ], # 1 -> 2
    "2 1" : [ [ 0, 0], [-1, 0], [-1,-2], [-1, 1], [-2,-2], [ 1, 1], [-1, 0] ], # 2 -> 1
    "2 3" : [ [ 0, 0], [ 0,-1], [ 0, 1], [ 0,-2], [-1, 1], [ 2,-2], [ 0,-1] ], # 2 -> 3
    "3 2" : [ [ 0, 0], [ 0, 1], [ 0, 2], [ 0,-1], [-2, 2], [ 1,-1], [ 0, 2] ], # 3 -> 2
    "3 0" : [ [ 0, 0], [-1, 0], [-1, 1], [-1,-2], [ 1, 1], [-2,-2], [-1, 0] ], # 3 -> 0
    "0 3" : [ [ 0, 0], [ 1, 0], [ 1,-1], [ 1, 2], [ 2, 2], [-1,-1], [ 1, 0] ], # 0 -> 3

    "0 2" : [ [ 0, 0], [ 1, 1], [ 0, 1], [ 1, 1], [ 1, 1], [ 1, 1], [ 1, 1] ], # 0 -> 2
    "2 0" : [ [ 0, 0], [-1,-1], [ 0,-1], [ 1, 1], [ 1, 1], [ 1, 1], [ 1, 1] ], # 2 -> 0
    "1 3" : [ [ 0, 0], [ 1,-1], [ 1, 0], [ 1, 1], [ 1, 1], [ 1, 1], [ 1, 1] ], # 1 -> 3
    "3 1" : [ [ 0, 0], [-1, 1], [-1, 0], [ 1, 1], [ 1, 1], [ 1, 1], [ 1, 1] ]  # 3 -> 1
    }

# 0 1 0
# 1 0 1
# 1 2 2
# 2 1 3
# 2 3 4
# 3 2 5
# 3 0 6
# 0 3 7

def draw_line(screen):
    for i in range(20):
        pg.draw.rect(screen, white, [BLOCK_SIZE*5, BLOCK_SIZE*(2+i), BLOCK_SIZE, BLOCK_SIZE])
        pg.draw.rect(screen, white, [BLOCK_SIZE*16, BLOCK_SIZE*(2+i), BLOCK_SIZE, BLOCK_SIZE])
    pg.draw.rect(screen, white, [BLOCK_SIZE*5, BLOCK_SIZE*2, BLOCK_SIZE*11, 1])
    for i in range(12):
        pg.draw.rect(screen, white, [BLOCK_SIZE*(5+i), BLOCK_SIZE*22, BLOCK_SIZE, BLOCK_SIZE])

def check_block_state(mino, x, y, stacks):
    blocks = mino.mino_to_block()
    states = []
    for block in blocks:
        if block["Y"] + y + 1 == 22:
            states.append(0)
        if block["X"] + x - 1 == 5:
            states.append(1)
        if block["X"] + x + 1 == 16:
            states.append(2)
        
        if block["X"] + x == 16 or block["X"] + x == 5 or block["Y"] + y == 22:
            states.append(3)

        for stack_line in stacks:
            if stack_line == []:
                continue
            for stack in stack_line:
                if block["Y"] + y == stack["Y"]:
                    if block["X"] + x - 1 == stack["X"]:
                        states.append(1)
                    if block["X"] + x + 1 == stack["X"]:
                        states.append(2)

                if block["X"] + x == stack["X"]:
                    if block["Y"] - y + 1 == stack["Y"]:
                        states.append(0)

                    if block["Y"] + y == stack["Y"]:
                        states.append(3)

    return states

def initiate():
    """
    return x, y, holding, spin, pas_spin, add_time
    """
    return 9, 0, False, 0, 0, 0

def escape_checker():
    global escape_time
    escape_time = 0
    while True:
        key = pg.key.get_pressed()
        while key[pg.K_ESCAPE]:
            escape_time += 1
            time.sleep(0.1)

        if escape_time > 3:
            return True

async def main():
    DAS = 3
    ADD = 10

    c_font = pg.font.SysFont("arial", BLOCK_SIZE, True, True)

    size = [BLOCK_SIZE*22, BLOCK_SIZE*25]
    screen = pg.display.set_mode(size)

    pg.display.set_caption("pytris")
    done = False
    clock = pg.time.Clock()

    bag = Bag()
    hold = Hold()
    stacks_objects = Stack()

    current_block = bag.pop_()

    x, y, holding, spin, pas_spin, add_time = initiate()

    spin_cnt = 0

    cnt = 0

    direction = 0
    das_time = 0
    das_cnt = 0

    count_d_line = 0

    # global escape_time
    # escape_timer = Thread(target=escape_checker)
    # escape_timer.daemon = True
    # escape_timer.start()

    start_time = int(time.time())
    while not done:
        # if escape_time > 10:
        #     done = True

        clock.tick(20)
        screen.fill(black)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == pg.KEYDOWN:
                das_cnt = 1
            elif event.type == pg.KEYUP:
                das_cnt = 0

        if das_cnt == 1:
            das_time += 1
        else:
            das_time = 0

        key = pg.key.get_pressed()

        if key[pg.K_x] or key[pg.K_z] or key[pg.K_a]:
            spin_cnt += 1
        
        if spin_cnt > 1:
            pas_spin = spin
            if key[pg.K_x]:
                spin += 1
            elif key[pg.K_z]:
                spin -= 1
            elif key[pg.K_a]:
                spin += 2
            spin_cnt = 0

        if spin > 3:
            spin -= 4
        if spin < 0:
            spin = spin + 4

        if pas_spin != spin:
            if current_block.color != light_blue:
                for y_m, x_m in KICK_TABLE[f"{pas_spin} {spin}"]:
                    x = x + x_m
                    y = y + y_m

                    srs_state = check_block_state(current_block, x_m, y_m, stacks_objects.stack_objects)
                    srs_is_3 = any(state == 3 for state in srs_state)

                    if not srs_is_3:
                        break

                    else:
                        x = x - x_m
                        y = y - y_m

            else:
                for y_m, x_m in I_KICK_TABLE[f"{pas_spin} {spin}"]:
                    x = x + x_m
                    y = y + y_m

                    srs_state = check_block_state(current_block, x_m, y_m, stacks_objects.stack_objects)
                    srs_is_3 = any(state == 3 for state in srs_state)

                    if not srs_is_3:
                        break

                    else:
                        x = x - x_m
                        y = y - y_m

            current_block.go_to(x, y)

        collide_states = check_block_state(current_block, 0, 0, stacks_objects.stack_objects)

        is_0 = any(state == 0 for state in collide_states)
        is_1 = any(state == 1 for state in collide_states)
        is_2 = any(state == 2 for state in collide_states)
        is_3 = any(state == 3 for state in collide_states)

        if not is_0 and (key[pg.K_DOWN] or cnt % 20 == 20):
            y += 1

        if not is_1 and key[pg.K_LEFT]:
            direction = -1
        elif not is_2 and key[pg.K_RIGHT]:
            direction = 1
        else:
            direction = 0

        if das_time == DAS:
            if direction == 1:
                x = 13
            if direction == -1:
                x = 6

            das_time = 0
        else:
            x += direction

        if (key[pg.K_LSHIFT] or key[pg.K_c]) and not holding:
            current_block = hold.change(current_block)
            holding = True
            if current_block is None:
                current_block = bag.pop_()

            spin = 0
            x = 9
            y = 0
            spin = 0
            pas_spin = 0

        if key[pg.K_SPACE] and is_0:
            add_time = 100
            time.sleep(0.1)

        current_block.go_to(x, y)
        current_block.draw_mino(spin)
        stacks_objects.draw_stack()
        count_d_line += stacks_objects.clear_line()
        hold.draw_holding_block()
        draw_line(screen)

        if add_time > ADD:
            stacks_objects.add(current_block)
            current_block = bag.pop_()

            x, y, holding, spin, pas_spin, add_time = initiate()

        cnt += 1
        text = c_font.render(str(count_d_line), True, white, black)
        screen.blit(text, (BLOCK_SIZE*12, BLOCK_SIZE*23))

        sec = int(time.time()) - start_time
        sec_text = c_font.render('{0}:{1}'.format(int(sec/60), sec%60), True, white, black)
        # print(sec, int(sec/60), sec%60)
        screen.blit(sec_text, (BLOCK_SIZE*10, BLOCK_SIZE*23))
        pg.display.flip()

        await asyncio.sleep(0)

asyncio.run(main())