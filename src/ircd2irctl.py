#!/usr/bin/env python
"""
Example input
    8819     4221      483     1624      429      597
      422      639      425      627      424     1632
      447      590      443      589      422      621
      447      596      444      589      467      592
      454      597      455     1621      449      615
      428      586      445      638      405     1631
      446     1624      449     1620      457     1627
      446      590      443      640      404      619
      399      621      439      596      449     1630
      456     1620      459     1617      447
Example output
pulse 8819
space 4221
pulse 483
space 1624
pulse 429
space 597
pulse 422
space 639
pulse 425
space 627
pulse 424
space 1632
pulse 447
space 590
pulse 443
space 589
pulse 422
space 621
pulse 447
space 596
pulse 444
space 589
pulse 467
space 592
pulse 454
space 597
pulse 455
space 1621
pulse 449
space 615
pulse 428
space 586
pulse 445
space 638
pulse 405
space 1631
pulse 446
space 1624
pulse 449
space 1620
pulse 457
space 1627
pulse 446
space 590
pulse 443
space 640
pulse 404
space 619
pulse 399
space 621
pulse 439
space 596
pulse 449
space 1630
pulse 456
space 1620
pulse 459
space 1617
pulse 447
"""


def main():
    i = 0
    while True:
        line = raw_input()
        if len(line) == 0:
            break
        l = line.split()
        for item in l:
            if i % 2 == 0:
                print('pulse {}'.format(item))
            else:
                print('space {}'.format(item))
            i += 1


if __name__ == '__main__':
    main()
