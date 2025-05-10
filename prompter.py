#!/usr/bin/env python3

def prompt_user_for_strategies(buckets):
    """
    Prompt the user to choose one of five conversion strategies for each bucket.

    :param buckets: list of bucket dicts with keys:
                    - 'max_size_mb': float
                    - 'files': list of Path
                    - 'strategies': list of strategy dicts with keys:
                        'label', 'quality', 'subsampling', 'optimize', 'estimated_size_mb'
    :return: dict mapping bucket_index (int) to chosen strategy_index (int)
    """
    chosen_map = {}
    for idx, bucket in enumerate(buckets):
        print(f"\nBucket {idx + 1}: <= {bucket['max_size_mb']} MB — {len(bucket['files'])} files")
        # List strategies
        for s_idx, strat in enumerate(bucket['strategies'], start=1):
            print(
                f"  {s_idx}. {strat['label']}  "
                f"(q={strat['quality']}, subsamp={strat['subsampling']}) -> "
                f"~{strat['estimated_size_mb']} MB\n"
                f"       ↳ {strat['description']}"
            )

        # Prompt user
        while True:
            choice = input(f"Choose strategy [1-5] for bucket {idx + 1}: ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(bucket['strategies']):
                chosen_map[idx] = int(choice) - 1
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
    return chosen_map
