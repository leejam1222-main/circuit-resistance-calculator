import math

class ResistanceCalculator:
    def __init__(self):
        self.resistances = []
        self.target_resistance = 0
        self.best_circuit = None
        self.best_total_resistance = float('inf')
        self.best_error = float('inf')
    
    def set_resistances(self, resistances):
        self.resistances = sorted(resistances)
    
    def set_target_resistance(self, target):
        self.target_resistance = target
    
    def calculate_series_resistance(self, resistors):
        return sum(resistors)
    
    def calculate_parallel_resistance(self, resistors):
        if not resistors:
            return 0
        return 1 / sum(1/r for r in resistors)
    
    def evaluate_circuit(self, circuit):
        if not circuit:
            return float('inf')
        
        if isinstance(circuit[0], list):
            # 병렬 연결
            parallel_resistances = [self.evaluate_circuit(branch) for branch in circuit]
            return self.calculate_parallel_resistance(parallel_resistances)
        else:
            # 직렬 연결
            return self.calculate_series_resistance(circuit)
    
    def format_circuit(self, circuit):
        if not circuit:
            return '[]'
        
        if isinstance(circuit[0], list):
            # 병렬 연결
            parallel_branches = [self.format_circuit(branch) for branch in circuit]
            return f"[{' || '.join(parallel_branches)}]"
        else:
            # 직렬 연결
            return f"[{' - '.join(map(str, circuit))}]"
    
    def find_best_combination(self, available_resistors, current_circuit=None, depth=0):
        if current_circuit is None:
            current_circuit = []
        
        # 현재 회로 평가
        if current_circuit:
            total_resistance = self.evaluate_circuit(current_circuit)
            error = abs(total_resistance - self.target_resistance)
            
            if error < self.best_error:
                self.best_circuit = current_circuit.copy()
                self.best_total_resistance = total_resistance
                self.best_error = error
        
        # 최대 깊이 제한
        if depth >= 3:
            return
        
        # 직렬 연결 시도
        for i, r in enumerate(available_resistors):
            remaining = available_resistors[i+1:]
            new_circuit = current_circuit + [r]
            self.find_best_combination(remaining, new_circuit, depth+1)
        
        # 병렬 연결 시도
        if len(available_resistors) >= 2:
            for i, r1 in enumerate(available_resistors[:-1]):
                for r2 in available_resistors[i+1:]:
                    parallel_branch = [[r1], [r2]]
                    remaining = [r for j, r in enumerate(available_resistors) if j != i and r != r2]
                    new_circuit = current_circuit + [parallel_branch]
                    self.find_best_combination(remaining, new_circuit, depth+1)
    
    def get_best_circuit(self):
        if self.best_circuit is None:
            return None, None, None
        
        error_percentage = (self.best_error / self.target_resistance) * 100
        return self.best_circuit, self.best_total_resistance, error_percentage

def main():
    calculator = ResistanceCalculator()
    
    # 저항 값 입력 받기
    print("저항 값들을 입력하세요 (최대 10개, 쉼표로 구분):")
    resistances_input = input().strip()
    resistances = [float(r.strip()) for r in resistances_input.split(',') if r.strip()]
    
    if not resistances or len(resistances) > 10:
        print("유효하지 않은 저항 개수입니다. 1-10개의 저항을 입력해주세요.")
        return
    
    # 목표 저항 값 입력 받기
    print("\n목표 저항 값을 입력하세요:")
    target = float(input().strip())
    
    # 계산 실행
    calculator.set_resistances(resistances)
    calculator.set_target_resistance(target)
    calculator.find_best_combination(calculator.resistances)
    
    # 결과 출력
    best_circuit, total_resistance, error_percentage = calculator.get_best_circuit()
    
    if best_circuit is None:
        print("\n유효한 회로를 찾을 수 없습니다.")
        return
    
    print("\n=== 결과 ===")
    print(f"입력 저항들: {resistances}")
    print(f"목표 저항: {target} Ω")
    print(f"회로 구성: {calculator.format_circuit(best_circuit)}")
    print(f"총 저항: {total_resistance:.2f} Ω")
    print(f"오차: {error_percentage:.2f}%")

if __name__ == "__main__":
    main()