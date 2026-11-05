# Business Requirements Specification (BRS)

**Product:** ReuseTwin (basket id `reusetwin`). Written from the basket description and this code; not reviewed by the owner.

## Business problem
Water scarcity pushes petrochemical and other heavy industry to reuse treated effluent through reverse osmosis (RO). Membranes foul; cleaning costs chemicals and downtime and slowly ages the membrane, while a fouled membrane costs energy. Operators clean on a fixed calendar.

## Objectives
| ID | Objective |
|----|-----------|
| BO-1 | Predict permeability decay and the days until a cleaning threshold |
| BO-2 | Choose cleaning timing that minimises total cost per m3 (energy, chemicals, downtime, replacement) |
| BO-3 | Keep working with noisy permeability measurements |
| BO-4 | Show how the schedule behaves when feed quality changes |

## Users
Utilities and process engineers of industrial water reuse plants.

## Scope
In: single-stage fouling twin, cleaning schedule, rate estimator. Out: multi-stage plant hydraulics, scaling chemistry, water quality prediction, control integration.

## Success measures (on plant data)
Cost per m3, number of cleanings, minimum permeability, forecast error of days-to-threshold, against the plant's calendar schedule.
