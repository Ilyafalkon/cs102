import dataclasses
import re
import typing as tp


@dataclasses.dataclass
class Route:
    path: str
    method: str
    func: tp.Callable

    def match(
        self, request_method: str, request_path: str
    ) -> tp.Tuple[bool, bool, tp.Optional[tp.List[str]], tp.Optional[tp.List[str]]]:
        if self.path[-1] == "/" and self.path != "/":
            self.path = self.path[:1]

        is_paths_match = False
        params_names = re.findall(r"\{([a-zA-Z_0-9]*)\}", self.path)
        if params_names:
            pattern = re.sub(r"(\{([a-zA-Z_0-9]*)\})", "([a-zA-Z_0-9]*)", self.path)
            values = re.findall(pattern, request_path)
            if values:
                params_values = list(values[0]) if isinstance(values[0], tuple) else values
            if params_values:
                is_paths_match = True
                if self.method == request_method:
                    return True, is_paths_match, params_names, params_values
        elif self.path == request_path:
            is_paths_match = True
            if self.method == request_method:
                return True, is_paths_match, [], []

        return False, is_paths_match, [], []
