from nsga2.evolution import Evolution
from nsga2.problem import Problem
import streamlit as st
import pandas as pd


class InfoGenerator:
    def __init__(self):
        pass
    def generate_num_of_variables(self, num_of_variables_text):
        try:
            return int(num_of_variables_text)
        except:
            return SyntaxError('Number of Variables must be an Interger')

    def generate_variables_range(self, variables_range_text, num_of_variables):
        if variables_range_text == '':
            return [(-1e5, 1e5) for _ in range(num_of_variables)]
        else:
            variables_range_list = variables_range_text.split('\n')
            try:
                for i in range(len(variables_range_list)):
                    temp = variables_range_list[i][1:-1].split(',')
                    variables_range_list[i] = (eval(temp[0]), eval(temp[1]))
            except:
                return SyntaxError('Variable Range must be Tuples of Float')
            if len(variables_range_list) < num_of_variables:
                return variables_range_list*num_of_variables
            elif len(variables_range_list) > num_of_variables:
                return SyntaxError('The Number of Variable Range must be equal to the Number of Variables')
            else:
                return variables_range_list
      
    def generate_response(self, input_text, variables_range):
        f_objective = input_text.split('\n')
        num_of_variables=len(variables_range)

        problem = Problem(num_of_variables=num_of_variables, objectives=f_objective, variables_range=variables_range, same_range=False)
        evo = Evolution(problem, num_of_generations=200, num_of_individuals=200, num_of_tour_particips=20, mutation_param=5)
        results = evo.evolve()

        best_features = [i.features for i in evo.plot_populations[-1]][0]
        best_objectives = [i.objectives for i in evo.plot_populations[-1]][0]
        output_text = f'Best result: {best_features}'
        if best_objectives[-1] > 0.01:
            output_text = f'Cannot find roots in feasible time \nBest result: {best_features}'
        st.text(output_text)

        self.generate_visual(evo.plot_populations)

    def generate_visual(self, plot_populations):
        func = [result[0] for result in plot_populations]
        num_of_variables = len(func[0].features)
        df = pd.DataFrame()
        df['Generation'] = range(1,len(func)+1) 
        for idx in range(num_of_variables):
            df[f'x{idx}'] = [x.features[idx] for x in func]
            df[f'f{idx}'] = [x.objectives[idx] for x in func]
        df.dropna()
        df.to_csv('results/result.csv')

        feature = [x for x in df.columns if x.startswith('x')]
        objective = [f for f in df.columns if f.startswith('f')]
        st.info('Visualization')
        st.line_chart(df, x='Generation', y=feature)
        st.line_chart(df, x='Generation', y=objective)

