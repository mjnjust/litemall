package org.linlinjava.litemall.admin;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;
import org.springframework.transaction.annotation.EnableTransactionManagement;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.Set;

@SpringBootApplication(scanBasePackages = {"org.linlinjava.litemall.db", "org.linlinjava.litemall.core", "org.linlinjava.litemall.admin"})
@MapperScan("org.linlinjava.litemall.db.dao")
@EnableTransactionManagement
@EnableScheduling
public class Application {

    public static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;

        TreeNode() {
        }

        TreeNode(int val) {
            this.val = val;
        }

        TreeNode(int val, TreeNode left, TreeNode right) {
            this.val = val;
            this.left = left;
            this.right = right;
        }
    }

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
//        System.out.println(coinChange(new int[]{186, 419, 83, 408}, 6249));
    }

    public boolean wordBreak(String s, List<String> wordDict) {
        return false;
    }


    public static int coinChange(int[] coins, int amount) {
        Arrays.sort(coins);
        if (amount == 0) {
            return 0;
        }
        if (amount < coins[0]) {
            return -1;
        }
        int[] dp = new int[amount + 1];
        for (int i = 0; i < dp.length; i++) {
            dp[i] = amount + 1;
        }
        dp[0] = 0;
        for (int i = 1; i <= amount; i++) {
            for (int j = 0; j < coins.length; j++) {
                if (coins[j] <= i) {
                    dp[i] = Math.min(dp[i], dp[i - coins[j]] + 1);
                }
            }
        }
        if (dp[amount] == 0 || dp[amount] > amount || dp[amount] < 0) {
            return -1;
        }
        return dp[amount];
    }

    public static int numSquares(int n) {
        if (n == 0) {
            return 0;
        }
        if (n == 1) {
            return 1;
        }
        if (n == 2) {
            return 2;
        }
        int[] dp = new int[n + 1];
        dp[0] = 0;
        dp[1] = 1;
        dp[2] = 2;
        for (int i = 3; i <= n; i++) {
            dp[i] = Integer.MAX_VALUE;
            for (int j = 1; j * j <= i; j++) {
                dp[i] = Math.min(dp[i], dp[i - j * j] + 1);
            }
        }
        return dp[n + 1];
    }

    public int rob(int[] nums) {
        int[] dp = new int[nums.length];
        dp[0] = nums[0];
        if (nums.length == 1) {
            return dp[0];
        }
        dp[1] = Math.max(nums[0], nums[1]);
        if (nums.length == 2) {
            return dp[1];
        }
        int max = Math.max(dp[0], dp[1]);
        for (int i = 2; i < nums.length; i++) {
            dp[i] = Math.max(dp[i - 1], dp[i - 2] + nums[i]);
            max = Math.max(max, dp[i]);
        }
        return max;
    }

    public List<List<Integer>> generate(int numRows) {
        List<List<Integer>> res = new LinkedList<>();
        if (numRows == 0) {
            return res;
        }
        res.add(Arrays.asList(new Integer[]{1}));
        if (numRows == 1) {
            return res;
        }
        res.add(Arrays.asList(new Integer[]{1, 1}));
        if (numRows == 2) {
            return res;
        }
        for (int i = 2; i < numRows; i++) {
            List<Integer> last = res.get(i - 1);
            List<Integer> r = new ArrayList<>();
            r.add(1);
            for (int t = 0; t < last.size() - 1; t++) {
                r.add(last.get(t) + last.get(t + 1));
            }
            r.add(1);
            res.add(r);
        }
        return res;
    }

    public static int climbStairs(int n) {
        if (n == 0) {
            return 0;
        }
        if (n == 1) {
            return 1;
        }
        if (n == 2) {
            return 2;
        }
        int[] dp = new int[n];
        dp[0] = 1;
        dp[1] = 2;
        for (int i = 2; i <= n - 1; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        return dp[n - 1];
    }

    public static int orangesRotting(int[][] grid) {
        Set<String> handle = new HashSet<>();
        Queue<Cell> queue = new LinkedList<>();
        boolean oo = false;
        int nums = 0;
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[i].length; j++) {
                if (grid[i][j] == 2) {
                    queue.offer(new Cell(i, j));
                    handle.add(i + ":" + j);
                } else if (grid[i][j] == 1) {
                    oo = true;
                    nums++;
                }
            }
        }

        if (queue.isEmpty()) {
            if (oo) {
                return -1;
            } else {
                return 0;
            }
        }

        int times = 0;
        while (!queue.isEmpty()) {
            int s = queue.size();
            for (int i = 0; i < s; i++) {
                Cell cell = queue.poll();
                int row = cell.row;
                int col = cell.col;
                // 上
                if (row - 1 >= 0 && grid[row - 1][col] == 1 && handle.add((row - 1) + ":" + col)) {
                    // 新数据 未处理
                    queue.offer(new Cell(row - 1, col));
                    nums--;
                }
                if (row + 1 <= grid.length - 1 && grid[row + 1][col] == 1 && handle.add((row + 1) + ":" + col)) {
                    queue.offer(new Cell(row + 1, col));
                    nums--;
                }
                if (col - 1 >= 0 && grid[row][col - 1] == 1 && handle.add(row + ":" + (col - 1))) {
                    queue.offer(new Cell(row, col - 1));
                    nums--;
                }
                if (col + 1 <= grid[0].length - 1 && grid[row][col + 1] == 1 && handle.add(row + ":" + (col + 1))) {
                    queue.offer(new Cell(row, col + 1));
                    nums--;
                }
            }
            if (!queue.isEmpty()) {
                times++;
            }
        }

        if (nums > 0) {
            return -1;
        }

        return times;
    }

    public static int numIslands() {
        return ii(new char[][]{{'1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '0', '1', '1'}, {'0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '0'}, {'1', '0', '1', '1', '1', '0', '0', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'}, {'1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'}, {'1', '0', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'}, {'1', '0', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '0', '1', '1', '1', '0', '1', '1', '1'}, {'0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '0', '1', '1', '1', '1'}, {'1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1'}, {'1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1'}, {'1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'}, {'0', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'}, {'1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'}, {'1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'}, {'1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1'}, {'1', '0', '1', '1', '1', '1', '1', '0', '1', '1', '1', '0', '1', '1', '1', '1', '0', '1', '1', '1'}, {'1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '1', '1', '0'}, {'1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '0', '1', '1', '1', '1', '0', '0'}, {'1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'}, {'1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'}, {'1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'}});
    }

    public static int ii(char[][] grid) {
        int s = 0;
        for (int i = 0; i < grid.length; i++) {
            for (int j = 0; j < grid[0].length; j++) {
                int res = mark(new Cell(i, j), grid);
                s = s + res;
            }
        }
        return s;
    }

    public static int mark(Cell cell, char[][] grid) {
        if (grid[cell.row][cell.col] == '2' || grid[cell.row][cell.col] == '3' || grid[cell.row][cell.col] == '0') {
            return 0;
        }
        Set<String> ss = new HashSet<>();
        Queue<Cell> queue = new LinkedList<>();
        queue.offer(cell);
        while (queue.size() > 0) {
            Cell tmp = queue.poll();
            if (!ss.contains(tmp.row + ":" + tmp.col)) {
                if (grid[tmp.row][tmp.col] == '1') {
                    grid[tmp.row][tmp.col] = '3';
                } else {
                    grid[tmp.row][tmp.col] = '2';
                }
                ss.add(tmp.row + ":" + tmp.col);
            } else {
                continue;
            }

            // 上 下 左 右
            if (tmp.row - 1 >= 0 && grid[tmp.row - 1][tmp.col] == '1') {
                queue.offer(new Cell(tmp.row - 1, tmp.col));
            }
            if (tmp.row + 1 <= grid.length - 1 && grid[tmp.row + 1][tmp.col] == '1') {
                queue.offer(new Cell(tmp.row + 1, tmp.col));
            }
            if (tmp.col - 1 >= 0 && grid[tmp.row][tmp.col - 1] == '1') {
                queue.offer(new Cell(tmp.row, tmp.col - 1));
            }
            if (tmp.col + 1 <= grid[0].length - 1 && grid[tmp.row][tmp.col + 1] == '1') {
                queue.offer(new Cell(tmp.row, tmp.col + 1));
            }
        }
        return 1;
    }

    public static class Cell {
        public int row;
        public int col;

        public Cell(int row, int col) {
            this.row = row;
            this.col = col;
        }

    }

    public static TreeNode buildTree(Integer[] arr) {
        if (arr == null || arr.length == 0 || arr[0] == null) {
            return null;
        }

        // 创建根节点
        TreeNode root = new TreeNode(arr[0]);
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);

        int index = 1; // 从数组的第二个元素开始

        while (!queue.isEmpty() && index < arr.length) {
            TreeNode current = queue.poll();

            // 处理左子节点
            if (index < arr.length && arr[index] != -1) {
                current.left = new TreeNode(arr[index]);
                queue.offer(current.left);
            }
            index++;

            // 处理右子节点
            if (index < arr.length && arr[index] != -1) {
                current.right = new TreeNode(arr[index]);
                queue.offer(current.right);
            }
            index++;
        }

        return root;
    }

    public static void dfs(TreeNode r) {
        System.out.println(r.val);
        if (r.left != null) {
            dfs(r.left);
        }
        if (r.right != null) {
            dfs(r.right);
        }
    }

}