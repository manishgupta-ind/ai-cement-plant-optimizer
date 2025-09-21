# Model-1 for clinker_free_lime\_%

This document provides a summary of the first machine learning model,
which is designed to predict the clinker_free_lime\_% KPI.

### Target KPI

- **Variable:** clinker_free_lime_pct

- **Process Stage:** Pyroprocessing (Kiln)

- **Objective:** To predict the percentage of free lime in clinker, a
  key quality metric.

### Model Logic and Dependencies

The clinker_free_lime\_% at any given time is a function of the raw
material and kiln conditions from approximately **5 hours earlier**. The
model is trained using **lagged input variables** to account for this
delay.

This model is a prime example of **cross-process optimization**, as it
uses the output of the upstream Blending process as an input to predict
a KPI for the Pyroprocessing stage. Specifically, the lagged
raw_meal_lsf_ratio is a critical feature.

### Input Features

The model uses the following variables as input features:

- raw_meal_lsf_ratio

- limestone_feed_rate_pct

- clay_feed_rate_pct

- iron_ore_feed_rate_pct

- bauxite_feed_rate_pct

- raw_meal_feed_rate_tph

- fuel_feed_rate_tph

- fuel_alt_substitution_rate_pct

- kiln_hood_pressure_mmH2O

- kiln_burner_air_flow_m3_hr

- kiln_main_drive_current_amp

The model does **not** use any variables from the grinding process, as
it is a downstream stage.

**Model-2: raw_meal_lsf_ratio**

This document provides a summary of the second machine learning model,
which is designed to predict the raw_meal_lsf_ratio KPI.

**Target KPI**

- **Variable:** raw_meal_lsf_ratio

- **Process Stage:** Blending

- **Objective:** To predict the Lime Saturation Factor, a critical
  quality metric for the raw meal.

**Model Logic and Dependencies**

This model predicts the raw meal\'s quality based on the real-time
composition of the raw material inputs. As the Blending process is the
first stage in the plant, this model uses **non-lagged** variables.

The output of this model is foundational for the subsequent stages. The
predicted raw_meal_lsf_ratio serves as a key input feature for
downstream models, such as the one for clinker_free_lime\_%, enabling
cross-process optimization.

**Input Features**

The model uses the following variables as input features, all of which
are from the Blending process:

- limestone_feed_rate_pct

- clay_feed_rate_pct

- iron_ore_feed_rate_pct

- bauxite_feed_rate_pct

This model does **not** use any variables from the Pyroprocessing or
Grinding processes, as they occur after the raw meal has been blended.

**Model-3: kiln_specific_thermal_energy_Kcal/kg_clinker**

This document provides a summary of the third machine learning model,
which is designed to predict the
kiln_specific_thermal_energy_Kcal/kg_clinker KPI.

**Target KPI**

- **Variable:** kiln_specific_thermal_energy_Kcal/kg_clinker

- **Process Stage:** Pyroprocessing (Kiln)

- **Objective:** To predict the energy efficiency of the kiln. The
  optimization goal is to minimize this value.

**Model Logic and Dependencies**

This model predicts the kiln\'s energy consumption based on the
real-time fuel inputs and overall kiln process conditions. Since changes
in these variables have a near-instantaneous effect on energy usage,
this model uses **non-lagged** variables.

This model is a core part of the **cross-process optimization**
strategy, helping the system understand the energy impact of adjustments
to fuel inputs and kiln operating conditions.

**Input Features**

The model uses the following variables as input features:

- raw_meal_feed_rate_tph

- fuel_feed_rate_tph

- fuel_alt_substitution_rate_pct

- kiln_hood_pressure_mmH2O

- kiln_burner_air_flow_m3/hr

- kiln_main_drive_current_amp

The model does **not** use any variables from the blending or grinding
processes, as they are not directly linked to the kiln\'s immediate
thermal energy consumption.

**Model-4: kiln_exit_nox_emissions_mg/Nm3**

This document provides a summary of the fourth machine learning model,
which is designed to predict the kiln_exit_nox_emissions_mg/Nm3 KPI.

**Target KPI**

- **Variable**: kiln_exit_nox_emissions_mg/Nm3

- **Process Stage**: Pyroprocessing (Kiln)

- **Objective**: To predict and minimize nitrogen oxide (NOx​) emissions,
  a key sustainability metric.

**Model Logic and Dependencies**

This model predicts the level of NOx​ emissions based on the real-time
fuel and air inputs to the kiln. Since changes to these variables have a
rapid effect on the kiln\'s combustion and emissions, this model uses
non-lagged variables from the Pyroprocessing stage.

The output of this model is critical for the plant\'s environmental and
sustainability goals. It helps the system proactively adjust process
parameters to keep emissions within compliant and optimal ranges.

**Input Features**

The model uses the following variables as input features, all of which
are directly related to the kiln\'s combustion process:

- fuel_feed_rate_tph: The amount of fuel fed to the kiln.

- fuel_alt_substitution_rate\_%: The percentage of alternative fuels
  used.

- kiln_burner_air_flow_m3/hr: The volume of air supplied to the main
  burner.

The model does not use any variables from the Blending or Grinding
processes, as they are not directly linked to the kiln\'s immediate
emissions.

**Model-5: mill_motor_power_draw_kW**

This document provides a summary of the fifth machine learning model,
which is designed to predict the mill_motor_power_draw_kW KPI.

**Target KPI**

- **Variable**: mill_motor_power_draw_kW

- **Process Stage**: Grinding

- **Objective**: To predict and minimize the electrical power consumed
  by the cement mill motor. The optimization goal is to reduce energy
  costs and improve overall plant efficiency.

**Model Logic and Dependencies**

This model predicts the power draw of the mill motor based on the
materials being fed into it. Since the motor\'s power consumption is a
direct, instantaneous function of its operational load, this model uses
real-time, non-lagged variables from the grinding process.

The output of this model is crucial for the Grinding process. By
accurately predicting power consumption, the system can provide
recommendations to operators on how to adjust feed rates to optimize
grinding efficiency and minimize electricity usage, a major operational
cost.

**Input Features**

The model uses the following variables as input features:

- clinker_feed_rate_tph: The rate at which clinker is fed to the mill.

- gypsum_feed_rate_tph: The rate at which gypsum is added to the mill.

- mill_recirculation_ratio\_%: The percentage of material that is
  recirculated back to the mill for re-grinding.

The model does not use variables from the upstream Blending or
Pyroprocessing stages, as the mill\'s power draw is primarily dependent
on the materials and operations within the Grinding process itself.

**Model-6: cement_fineness_blaine_cm2/g**

This document provides a summary of the sixth machine learning model,
which is designed to predict the cement_fineness_blaine_cm2/g KPI.

**Target KPI**

- **Variable**: cement_fineness_blaine_cm2/g

- **Process Stage**: Grinding

- **Objective**: To predict and maintain the optimal fineness of the
  finished cement. Cement fineness is a critical quality parameter that
  affects its strength development, workability, and hydration
  properties.

**Model Logic and Dependencies**

This model predicts the final fineness of the cement based on the
current grinding conditions. The fineness is a direct result of how long
and how much the material is ground. Therefore, this model uses
real-time, non-lagged variables from the Grinding process.

The output of this model is crucial for quality control. It provides a
predictive measure of the final product\'s quality, allowing for
proactive adjustments to the grinding process to ensure the cement meets
the required specifications before it is stored or shipped.

**Input Features**

The model uses the following variables as input features:

- clinker_feed_rate_tph: The rate at which clinker is fed to the mill.

- gypsum_feed_rate_tph: The rate at which gypsum is added to the mill.

- mill_recirculation_ratio\_%: The percentage of material that is
  recirculated back to the mill for re-grinding.

The model does not use variables from the upstream Blending or
Pyroprocessing stages, as the final cement fineness is determined
entirely by the Grinding process.

**Model-7: mill_specific_electrical_energy_kWh/ton_cement**

This document provides a summary of the seventh and final machine
learning model, which is designed to predict the
mill_specific_electrical_energy_kWh/ton_cement KPI.

**Target KPI**

- **Variable**: mill_specific_electrical_energy_kWh/ton_cement

- **Process Stage**: Grinding

- **Objective**: To predict and minimize the energy required to grind
  one ton of cement. This is a crucial metric for measuring the overall
  energy efficiency of the Grinding process and directly impacts the
  plant\'s operational costs.

**Model Logic and Dependencies**

This model predicts the energy consumption per ton of cement produced.
This value is a function of the mill\'s power draw and the production
rate, both of which are determined by the input feed rates and
recirculation. Therefore, this model uses real-time, non-lagged
variables from the Grinding process.

The output of this model provides a key indicator for cost-effective
operations. By predicting this value, the system can provide
recommendations to optimize the mill\'s feed and recirculation settings
to ensure the target fineness is met with the lowest possible energy
consumption.

**Input Features**

The model uses the following variables as input features:

- clinker_feed_rate_tph: The rate at which clinker is fed to the mill.

- gypsum_feed_rate_tph: The rate at which gypsum is added to the mill.

- mill_recirculation_ratio\_%: The percentage of material that is
  recirculated back to the mill for re-grinding.

- mill_motor_power_draw_kW: The electrical power consumed by the mill
  motor.

The model does not use variables from the upstream Blending or
Pyroprocessing stages, as the grinding efficiency and energy consumption
are isolated to the Grinding process.
