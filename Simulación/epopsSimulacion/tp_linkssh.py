def tplink_id(b_root, dp ,ds,iptp):
    for i in iptp:
        if i in ds.keys():
            try:
               i_c = dp[i][0].index(b_root)
               dp[i][0][i_c] = ds[i]
            except ValueError as e:
               print(f"Error: {e}")

        else:
            try:
               i_c = dp[i][0].index(b_root)
               dp[i][0][i_c] = "11111111"
            except ValueError as e:
               print(f"Error: {e}")
    return dp
