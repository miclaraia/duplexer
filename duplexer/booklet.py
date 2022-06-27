import math
from typing import List, Union


class Booklet:
    @classmethod
    def get_mapping(cls, N):
        page_mapping = cls._init_page_mapping(N)

        # page mapping [i]=j: printed page j is at position i in the booklet
        # now reverse the mapping, so we have the order of pages to print in
        # booklet
        mapping: List[Union[str, int]] = [-1 for _ in page_mapping]
        for i, p in enumerate(page_mapping):
            if i < N:
                mapping[p] = i
            else:
                mapping[p] = 'blank'

        print(mapping)
        return mapping

    @staticmethod
    def _init_page_mapping(N):
        N_ = 4*math.ceil(N/4)
        mapping = [-1 for _ in range(N_)]

        right = N_//2
        left = right - 1
        for i in range(0, N_, 4):
            mapping[left] = i
            mapping[right] = i+1
            mapping[right+1] = i+2
            mapping[left-1] = i+3

            left -= 2
            right += 2

        print(mapping)
        # mapping[i] = j: printed page j is at position i in the booklet

        return mapping


def main():
    try:
        Booklet.get_mapping(8)
        Booklet.get_mapping(10)
    except Exception:
        import traceback
        import pdb
        traceback.print_exc()
        pdb.post_mortem()


if __name__ == '__main__':
    main()

