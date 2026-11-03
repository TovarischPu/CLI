from typing import Callable, Dict, List, Set


class DependencyGraph:
    def __init__(self) -> None:
        self.adjacency_list: Dict[str, List[str]] = {}

    def add_edge(self, source: str, target: str) -> None:
        if source not in self.adjacency_list:
            self.adjacency_list[source] = []
        if target not in self.adjacency_list[source]:
            self.adjacency_list[source].append(target)
        if target not in self.adjacency_list:
            self.adjacency_list[target] = []


class GraphBuilder:
    def __init__(
        self,
        max_depth: int,
        filter_str: str,
        fetch_func: Callable[[str], List[str]],
    ) -> None:
        self.max_depth = max_depth
        self.filter_str = filter_str
        self.fetch_func = fetch_func
        self.graph = DependencyGraph()
        self.visited: Set[str] = set()

    def _is_valid_package(self, pkg: str) -> bool:
        if pkg in self.visited:
            return False
        if self.filter_str and self.filter_str in pkg:
            return False
        return True

    def _process_level(self, current_level: List[str], depth: int) -> None:
        if not current_level or depth > self.max_depth:
            return

        next_level: List[str] = []
        for pkg in current_level:
            self.visited.add(pkg)
            deps = self.fetch_func(pkg)
            
            for dep in deps:
                if self._is_valid_package(dep):
                    self.graph.add_edge(pkg, dep)
                    next_level.append(dep)
                    self.visited.add(dep)

        self._process_level(next_level, depth + 1)

    def build(self, start_pkg: str) -> DependencyGraph:
        if not self._is_valid_package(start_pkg):
            return self.graph
        
        self.visited.add(start_pkg)
        self._process_level([start_pkg], 1)
        return self.graph


def parse_test_file(file_path: str) -> Dict[str, List[str]]:
    dependencies: Dict[str, List[str]] = {}
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or ":" not in line:
                continue
            
            parts = line.split(":", 1)
            pkg = parts[0].strip()
            deps_str = parts[1].strip()
            
            if deps_str:
                deps = [d.strip() for d in deps_str.split(",")]
            else:
                deps = []
                
            dependencies[pkg] = deps
    return dependencies