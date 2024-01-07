import streamlit as st
from gui.generate_info import InfoGenerator

class Window:
   def __init__(self) -> None:
      pass
   def __call__(self):
      st.set_page_config(page_title="System of Equations Solver:exclamation:")
      st.title('System of Equations Solver:exclamation:') 

      info_generator = InfoGenerator()

      num_of_variables_text = st.text_input('Number of Variables', placeholder='Eg: 2')
      num_of_variables = info_generator.generate_num_of_variables(num_of_variables_text)
      if type(num_of_variables) == int:
         variables_range_text = st.text_area('Variable Ranges (Optional)', placeholder='Eg:\n(-1e5, 1e5)\n(-10, 10)')
         variables_range = info_generator.generate_variables_range(variables_range_text, num_of_variables)
         st.text(variables_range)
         if variables_range:
            equations_text = st.text_area('System of Equations:', placeholder='Eg:\nx0 + x1 = 2\nx0 - x1 = 0')
            if equations_text:
               info_generator.generate_response(equations_text, variables_range)
      else: st.text(num_of_variables)
