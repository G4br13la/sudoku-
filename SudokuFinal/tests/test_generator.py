from instances.generator import count_solutions, generate_puzzle


def test_generator_is_reproducible_and_unique():
    first = generate_puzzle("diagonal", "Facil", seed=123)
    second = generate_puzzle("diagonal", "Facil", seed=123)
    assert first == second
    assert count_solutions(first, "diagonal", limit=2) == 1


def test_all_six_catalog_instances_have_unique_solutions():
    from instances.catalog import get_puzzle
    for variant in ("clasico", "diagonal"):
        for difficulty in ("Facil", "Medio", "Dificil"):
            assert count_solutions(get_puzzle(variant, difficulty), variant, limit=2) == 1


def test_randomized_full_solutions_vary_beyond_digit_permutations():
    import random
    from instances.generator import _generate_solution
    from environment.constraints import validate_complete_board

    for variant in ('clasico', 'diagonal'):
        first_rows = set()
        canonical_grids = set()
        for seed in range(8):
            solution = _generate_solution(variant, random.Random(seed))
            assert validate_complete_board(solution, variant) == []
            first_rows.add(tuple(solution[0]))
            # Si solo se permutaran los dígitos, esta representación sería igual.
            mapping = {value: index for index, value in enumerate(solution[0], 1)}
            canonical_grids.add(tuple(mapping[value] for row in solution for value in row))
        assert len(first_rows) == 8
        assert len(canonical_grids) == 8


def test_generated_puzzles_preserve_levels_and_unique_solution():
    from instances.generator import DIFFICULTY_CLUES
    from instances.catalog import clue_count
    from environment.constraints import validate_partial_board

    for variant in ('clasico', 'diagonal'):
        for difficulty, target in DIFFICULTY_CLUES.items():
            boards = [generate_puzzle(variant, difficulty, seed) for seed in (31, 32, 33)]
            assert len({tuple(map(tuple, board)) for board in boards}) == 3
            for board in boards:
                assert clue_count(board) == target
                assert validate_partial_board(board, variant) == []
                assert count_solutions(board, variant, limit=2) == 1
