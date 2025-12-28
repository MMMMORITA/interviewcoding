import math
from typing import List, Optional, Any, Callable, Set, Tuple
from dataclasses import dataclass, field
from collections import deque

# ==========================================
# 1. 基础数据结构定义
# ==========================================

@dataclass
class ThoughtNode:
    """
    思维树节点
    state: 当前的数字和表达式列表，例如 [(3, "3"), (8, "8")]
    """
    state: List[Tuple[float, str]]
    parent: Optional['ThoughtNode'] = None
    score: float = 0.0
    depth: int = 0
    
    def __repr__(self):
        return f"Node(depth={self.depth}, score={self.score:.2f}, state={self.state})"

# ==========================================
# 2. ToT 核心框架实现
# ==========================================

class TreeOfThoughts:
    """Tree of Thoughts 通用框架"""
    
    def __init__(
        self,
        thought_generator: Callable[[Any], List[Any]],
        state_evaluator: Callable[[Any], float],
        goal_checker: Callable[[Any], bool],
        strategy: str = 'bfs'
    ):
        self.thought_generator = thought_generator
        self.state_evaluator = state_evaluator
        self.goal_checker = goal_checker
        self.strategy = strategy.lower()
        self.visited_states = set()

    def search(self, initial_state: Any) -> Optional[ThoughtNode]:
        """执行搜索"""
        root = ThoughtNode(state=initial_state, depth=0)
        root.score = self.state_evaluator(initial_state)
        
        if self.strategy == 'bfs':
            return self._bfs(root)
        elif self.strategy == 'dfs':
            return self._dfs(root)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

    def _bfs(self, root: ThoughtNode) -> Optional[ThoughtNode]:
        """广度优先搜索"""
        queue = deque([root])
        
        while queue:
            current_node = queue.popleft()
            
            # 检查是否达到目标
            if self.goal_checker(current_node.state):
                return current_node
            
            # 剪枝：如果当前状态评分极低（例如非法），则不扩展
            if current_node.score <= 0.0:
                continue

            # 生成可能的下一步思维
            next_states = self.thought_generator(current_node.state)
            
            for state in next_states:
                # 简单的状态去重 key: 对数值进行排序后转tuple
                # 注意：这里只对比数值，忽略表达式字符串的差异
                vals = tuple(sorted([round(x[0], 5) for x in state]))
                if vals in self.visited_states:
                    continue
                self.visited_states.add(vals)

                score = self.state_evaluator(state)
                child = ThoughtNode(
                    state=state,
                    parent=current_node,
                    score=score,
                    depth=current_node.depth + 1
                )
                queue.append(child)
        
        return None

    def _dfs(self, root: ThoughtNode) -> Optional[ThoughtNode]:
        """深度优先搜索"""
        stack = [root]
        
        while stack:
            current_node = stack.pop()
            
            if self.goal_checker(current_node.state):
                return current_node
            
            if current_node.score <= 0.0:
                continue

            # 生成子状态
            next_states = self.thought_generator(current_node.state)
            
            # 为了保持DFS的一般顺序，可以反转一下列表压栈
            for state in reversed(next_states):
                vals = tuple(sorted([round(x[0], 5) for x in state]))
                if vals in self.visited_states:
                    continue
                self.visited_states.add(vals)

                score = self.state_evaluator(state)
                child = ThoughtNode(
                    state=state,
                    parent=current_node,
                    score=score,
                    depth=current_node.depth + 1
                )
                stack.append(child)
        
        return None

# ==========================================
# 3. 24点特定逻辑实现
# ==========================================

class Point24Solver:
    """24点求解器"""
    
    def __init__(self, strategy='bfs'):
        self.tot = TreeOfThoughts(
            thought_generator=self._generate_thoughts,
            state_evaluator=self._evaluate_state,
            goal_checker=self._check_goal,
            strategy=strategy
        )

    def _generate_thoughts(self, current_state: List[Tuple[float, str]]) -> List[List[Tuple[float, str]]]:
        """
        生成器：任选两个数进行加减乘除，生成新状态
        State格式: [(val1, exp1), (val2, exp2), ...]
        """
        next_states = []
        n = len(current_state)
        
        if n < 2:
            return []

        # 遍历所有两两组合
        for i in range(n):
            for j in range(n):
                if i == j: 
                    continue
                
                v1, exp1 = current_state[i]
                v2, exp2 = current_state[j]
                
                # 剩下的数字列表
                remaining = [current_state[k] for k in range(n) if k != i and k != j]
                
                # 1. 加法 (只处理 i < j 以避免重复，因为 a+b = b+a)
                if i < j:
                    next_states.append(remaining + [(v1 + v2, f"({exp1} + {exp2})")])
                
                # 2. 乘法 (只处理 i < j)
                if i < j:
                    next_states.append(remaining + [(v1 * v2, f"({exp1} * {exp2})")])
                
                # 3. 减法 (a - b) - 不交换，需要处理两种情况，这里通过两层循环自然覆盖
                next_states.append(remaining + [(v1 - v2, f"({exp1} - {exp2})")])
                
                # 4. 除法 (a / b) - 需要检查分母
                if abs(v2) > 1e-6: # 避免除以0
                    next_states.append(remaining + [(v1 / v2, f"({exp1} / {exp2})")])
                    
        return next_states

    def _evaluate_state(self, state: List[Tuple[float, str]]) -> float:
        """
        评估函数：如果找到24返回1.0，否则返回基于距离的启发式分数
        """
        if not state:
            return 0.0
        
        # 检查是否包含24
        for v, _ in state:
            if math.isclose(v, 24.0, abs_tol=1e-5):
                return 1.0
        
        # 启发式：找到最接近24的数字
        # 分数范围 (0, 1)
        min_diff = min(abs(v - 24.0) for v, _ in state)
        return 1.0 / (1.0 + min_diff)

    def _check_goal(self, state: List[Tuple[float, str]]) -> bool:
        """目标检测：剩下一个数字且等于24"""
        if len(state) == 1:
            val = state[0][0]
            return math.isclose(val, 24.0, abs_tol=1e-5)
        return False

    def solve(self, numbers: List[int]) -> Optional[str]:
        """
        求解主入口
        """
        # 1. 转换输入为初始状态格式: [(3, "3"), (8, "8"), ...]
        initial_state = [(float(x), str(x)) for x in numbers]
        
        # 2. 重置 ToT 的访问记录 (针对新的求解)
        self.tot.visited_states = set()
        
        # 3. 执行搜索
        result_node = self.tot.search(initial_state)
        
        # 4. 格式化输出
        if result_node:
            # result_node.state 应该是 [(24.0, "(...)")]
            expression = result_node.state[0][1]
            # 去掉最外层的括号（美观）
            if expression.startswith("(") and expression.endswith(")"):
                expression = expression[1:-1]
            return f"{expression} = 24"
        else:
            return None

# ==========================================
# 4. 测试代码
# ==========================================
if __name__ == "__main__":
    # 使用 BFS 策略实例化
    solver = Point24Solver(strategy='bfs')
    
    test_cases = [
        [3, 3, 8, 8],  # 经典难例: 8/(3-8/3)
        [1, 1, 1, 1],  # 无解
        [1, 2, 3, 4],  # 简单: 1*2*3*4
        [5, 5, 5, 1],  # 分数运算: (5-1/5)*5
    ]
    
    print("=== 24点 ToT Solver 测试 ===")
    for nums in test_cases:
        result = solver.solve(nums)
        if result:
            print(f"输入: {nums} -> 解答: {result}")
        else:
            print(f"输入: {nums} -> 无解")