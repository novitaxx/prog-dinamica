class WorkforceModel:
    def __init__(self, requirements, cost_excess, cost_fixed, cost_new):
        """
        Inicializa el modelo de fuerza laboral.

        :param requirements: Lista de trabajadores requeridos por semana.
        :param cost_excess: Costo por mantener un trabajador excedente por semana.
        :param cost_fixed: Costo fijo por contratar nuevos trabajadores.
        :param cost_new: Costo variable por cada trabajador nuevo contratado.
        """
        self.requirements = requirements
        self.cost_excess = cost_excess
        self.cost_fixed = cost_fixed
        self.cost_new = cost_new
        self.weeks = len(requirements)
        self.max_workers = max(requirements)
        self.dp = [[float('inf')] * (self.max_workers + 1) for _ in range(self.weeks + 1)]
        self.path = [[None] * (self.max_workers + 1) for _ in range(self.weeks + 1)]

    def solve(self):
        """
        Resuelve el problema utilizando programación dinámica.
        """
        # Caso base: Costo 0 al final sin trabajadores.
        for workers in range(self.max_workers + 1):
            self.dp[self.weeks][workers] = 0

        # Iterar en reversa desde la última semana
        for week in range(self.weeks - 1, -1, -1):
            for workers in range(self.max_workers + 1):
                for new_workers in range(self.max_workers + 1):
                    total_workers = workers + new_workers
                    if total_workers > self.max_workers:
                        continue  # Evitar índices fuera de rango
                    if total_workers >= self.requirements[week]:
                        # Calcular costos
                        cost_excess = (total_workers - self.requirements[week]) * self.cost_excess
                        cost_hiring = self.cost_fixed + new_workers * self.cost_new if new_workers > 0 else 0
                        next_cost = self.dp[week + 1][total_workers]
                        total_cost = cost_excess + cost_hiring + next_cost

                        # Actualizar DP y ruta óptima
                        if total_cost < self.dp[week][workers]:
                            self.dp[week][workers] = total_cost
                            self.path[week][workers] = new_workers

    def reconstruct_path(self):
        """
        Reconstruye la solución óptima.

        :return: Lista de trabajadores contratados cada semana.
        """
        workers = 0
        hiring_plan = []
        for week in range(self.weeks):
            new_workers = self.path[week][workers]
            hiring_plan.append(new_workers)
            workers += new_workers
        return hiring_plan

    def display_results(self):
        """
        Muestra los resultados del modelo.
        """
        print("Tabla de costos mínimos (DP):")
        for week in range(self.weeks + 1):
            print(f"Semana {week}: {self.dp[week]}")

        print("\nSolución óptima:")
        hiring_plan = self.reconstruct_path()
        for week, hired in enumerate(hiring_plan, start=1):
            print(f"Semana {week}: Contratar {hired} trabajadores.")

        print(f"\nCosto total mínimo: {self.dp[0][0]}")


# Parámetros del problema
requirements = [5, 7, 8, 4, 6]
cost_excess = 300
cost_fixed = 400
cost_new = 200

# Resolver problema
model = WorkforceModel(requirements, cost_excess, cost_fixed, cost_new)
model.solve()
model.display_results()
