# 📊 GANTT SIMPLIFIÉ - PROJET ROBOCUP

## 📅 DIVISION DU PROJET POUR DIAGRAMME DE GANTT

### Vue d'ensemble : 14 semaines au total

```
PHASE 1 : ROS1 (Semaines 1-6)
PHASE 2 : ROS2 (Semaines 7-14)
```

---

## 📋 FORMAT POUR GANTT (CSV/Excel)

### Structure des colonnes :
| Tâche | Responsable | Début | Fin | Durée | Dépendances | Phase |

---

## 📊 DONNÉES POUR GANTT

### 🟦 PHASE 1 : ROS1 OPÉRATIONNEL (6 semaines)

#### Semaine 1-2 : Setup et Tests de Base

| ID | Tâche | Responsable | Semaine Début | Semaine Fin | Durée (sem) | Dépendances |
|----|-------|-------------|---------------|-------------|-------------|-------------|
| 1.0 | **SETUP ENVIRONNEMENT** | Tous | 1 | 2 | 2 | - |
| 1.1 | Configuration Docker | Personne 4 | 1 | 1 | 1 | - |
| 1.2 | Compilation ROS1 | Personne 4 | 1 | 2 | 2 | 1.1 |
| 1.3 | Test LIDAR | Personne 1 | 1 | 2 | 2 | 1.1 |
| 1.4 | Test Caméra 8MP | Personne 2 | 1 | 2 | 2 | 1.1 |
| 1.5 | Upload Arduino + Test Servos | Personne 3 | 1 | 2 | 2 | 1.1 |
| 1.6 | Test Moteurs Sabertooth | Personne 4 | 2 | 2 | 1 | 1.2 |

#### Semaine 3-4 : Intégration Composants

| ID | Tâche | Responsable | Semaine Début | Semaine Fin | Durée (sem) | Dépendances |
|----|-------|-------------|---------------|-------------|-------------|-------------|
| 2.0 | **INTÉGRATION COMPOSANTS** | Tous | 3 | 4 | 2 | 1.0 |
| 2.1 | SLAM avec hector_mapping | Personne 1 | 3 | 4 | 2 | 1.3 |
| 2.2 | Caméra RealSense RGBD | Personne 2 | 3 | 4 | 2 | 1.4 |
| 2.3 | ROS Serial Arduino ↔ ROS | Personne 3 | 3 | 4 | 2 | 1.5 |
| 2.4 | Odométrie | Personne 4 | 3 | 4 | 2 | 1.6 |

#### Semaine 5-6 : Navigation et Finalisation

| ID | Tâche | Responsable | Semaine Début | Semaine Fin | Durée (sem) | Dépendances |
|----|-------|-------------|---------------|-------------|-------------|-------------|
| 3.0 | **NAVIGATION AUTONOME** | Tous | 5 | 6 | 2 | 2.0 |
| 3.1 | Navigation autonome | Personne 1 | 5 | 6 | 2 | 2.1 |
| 3.2 | Traitement images OpenCV | Personne 2 | 5 | 6 | 2 | 2.2 |
| 3.3 | Interface Python contrôle bras | Personne 3 | 5 | 6 | 2 | 2.3 |
| 3.4 | Intégration complète ROS1 | Personne 4 | 5 | 6 | 2 | 2.4 |
| 3.5 | **DÉMONSTRATION ROS1** | Tous | 6 | 6 | 1 | 3.0 |

---

### 🟩 PHASE 2 : MIGRATION ROS2 (8 semaines)

#### Semaine 7-8 : Architecture ROS2

| ID | Tâche | Responsable | Semaine Début | Semaine Fin | Durée (sem) | Dépendances |
|----|-------|-------------|---------------|-------------|-------------|-------------|
| 4.0 | **SETUP ROS2** | Tous | 7 | 8 | 2 | 3.5 |
| 4.1 | Migration LIDAR → urg_node2 | Personne 1 | 7 | 8 | 2 | 4.0 |
| 4.2 | Migration Caméras → cv_bridge | Personne 2 | 7 | 8 | 2 | 4.0 |
| 4.3 | Micro-ROS Arduino | Personne 3 | 7 | 8 | 2 | 4.0 |
| 4.4 | Architecture workspace ROS2 | Personne 4 | 7 | 8 | 2 | 4.0 |

#### Semaine 9-10 : Migration Fonctionnalités

| ID | Tâche | Responsable | Semaine Début | Semaine Fin | Durée (sem) | Dépendances |
|----|-------|-------------|---------------|-------------|-------------|-------------|
| 5.0 | **MIGRATION FONCTIONS** | Tous | 9 | 10 | 2 | 4.0 |
| 5.1 | SLAM Toolbox ROS2 | Personne 1 | 9 | 10 | 2 | 4.1 |
| 5.2 | Pipeline vision ROS2 | Personne 2 | 9 | 10 | 2 | 4.2 |
| 5.3 | Interface Python ROS2 (rclpy) | Personne 3 | 9 | 10 | 2 | 4.3 |
| 5.4 | Moteurs + Odométrie ROS2 | Personne 4 | 9 | 10 | 2 | 4.4 |

#### Semaine 11-12 : Navigation ROS2

| ID | Tâche | Responsable | Semaine Début | Semaine Fin | Durée (sem) | Dépendances |
|----|-------|-------------|---------------|-------------|-------------|-------------|
| 6.0 | **NAVIGATION ROS2** | Tous | 11 | 12 | 2 | 5.0 |
| 6.1 | Code navigation ROS2 (rclcpp) | Personne 1 | 11 | 12 | 2 | 5.1 |
| 6.2 | Finalisation pipeline vision | Personne 2 | 11 | 12 | 2 | 5.2 |
| 6.3 | URDF + RViz2 | Personne 3 | 11 | 12 | 2 | 5.3 |
| 6.4 | Launch files Python | Personne 4 | 11 | 12 | 2 | 5.4 |

#### Semaine 13-14 : Tests et Optimisation

| ID | Tâche | Responsable | Semaine Début | Semaine Fin | Durée (sem) | Dépendances |
|----|-------|-------------|---------------|-------------|-------------|-------------|
| 7.0 | **TESTS FINAUX** | Tous | 13 | 14 | 2 | 6.0 |
| 7.1 | Tests + Optimisation Navigation | Personne 1 | 13 | 14 | 2 | 6.1 |
| 7.2 | Tests + Optimisation Vision | Personne 2 | 13 | 14 | 2 | 6.2 |
| 7.3 | Tests + Optimisation Bras | Personne 3 | 13 | 14 | 2 | 6.3 |
| 7.4 | Tests intégration complète | Personne 4 | 13 | 14 | 2 | 6.4 |
| 7.5 | Documentation finale | Tous | 14 | 14 | 1 | 7.0 |
| 7.6 | **DÉMONSTRATION FINALE** | Tous | 14 | 14 | 1 | 7.5 |

---

## 📊 FORMAT CSV POUR IMPORT

```csv
ID,Tâche,Responsable,Début,Fin,Durée,Phase,Couleur
1.0,Setup Environnement,Tous,S1,S2,2,Phase 1,#3498db
1.1,Configuration Docker,Personne 4,S1,S1,1,Phase 1,#3498db
1.2,Compilation ROS1,Personne 4,S1,S2,2,Phase 1,#3498db
1.3,Test LIDAR,Personne 1,S1,S2,2,Phase 1,#3498db
1.4,Test Caméra 8MP,Personne 2,S1,S2,2,Phase 1,#3498db
1.5,Upload Arduino + Servos,Personne 3,S1,S2,2,Phase 1,#3498db
1.6,Test Moteurs Sabertooth,Personne 4,S2,S2,1,Phase 1,#3498db
2.0,Intégration Composants,Tous,S3,S4,2,Phase 1,#2ecc71
2.1,SLAM hector_mapping,Personne 1,S3,S4,2,Phase 1,#2ecc71
2.2,Caméra RealSense,Personne 2,S3,S4,2,Phase 1,#2ecc71
2.3,ROS Serial,Personne 3,S3,S4,2,Phase 1,#2ecc71
2.4,Odométrie,Personne 4,S3,S4,2,Phase 1,#2ecc71
3.0,Navigation Autonome,Tous,S5,S6,2,Phase 1,#f39c12
3.1,Navigation autonome,Personne 1,S5,S6,2,Phase 1,#f39c12
3.2,Traitement images,Personne 2,S5,S6,2,Phase 1,#f39c12
3.3,Interface contrôle bras,Personne 3,S5,S6,2,Phase 1,#f39c12
3.4,Intégration ROS1,Personne 4,S5,S6,2,Phase 1,#f39c12
3.5,DÉMONSTRATION ROS1,Tous,S6,S6,1,Phase 1,#e74c3c
4.0,Setup ROS2,Tous,S7,S8,2,Phase 2,#9b59b6
4.1,Migration LIDAR,Personne 1,S7,S8,2,Phase 2,#9b59b6
4.2,Migration Caméras,Personne 2,S7,S8,2,Phase 2,#9b59b6
4.3,Micro-ROS Arduino,Personne 3,S7,S8,2,Phase 2,#9b59b6
4.4,Architecture ROS2,Personne 4,S7,S8,2,Phase 2,#9b59b6
5.0,Migration Fonctions,Tous,S9,S10,2,Phase 2,#1abc9c
5.1,SLAM Toolbox,Personne 1,S9,S10,2,Phase 2,#1abc9c
5.2,Pipeline vision ROS2,Personne 2,S9,S10,2,Phase 2,#1abc9c
5.3,Interface Python rclpy,Personne 3,S9,S10,2,Phase 2,#1abc9c
5.4,Moteurs + Odom ROS2,Personne 4,S9,S10,2,Phase 2,#1abc9c
6.0,Navigation ROS2,Tous,S11,S12,2,Phase 2,#34495e
6.1,Code navigation rclcpp,Personne 1,S11,S12,2,Phase 2,#34495e
6.2,Finalisation vision,Personne 2,S11,S12,2,Phase 2,#34495e
6.3,URDF + RViz2,Personne 3,S11,S12,2,Phase 2,#34495e
6.4,Launch files Python,Personne 4,S11,S12,2,Phase 2,#34495e
7.0,Tests Finaux,Tous,S13,S14,2,Phase 2,#16a085
7.1,Tests Navigation,Personne 1,S13,S14,2,Phase 2,#16a085
7.2,Tests Vision,Personne 2,S13,S14,2,Phase 2,#16a085
7.3,Tests Bras,Personne 3,S13,S14,2,Phase 2,#16a085
7.4,Tests Intégration,Personne 4,S13,S14,2,Phase 2,#16a085
7.5,Documentation,Tous,S14,S14,1,Phase 2,#27ae60
7.6,DÉMONSTRATION FINALE,Tous,S14,S14,1,Phase 2,#c0392b
```

---

## 📈 VISUALISATION SIMPLIFIÉE

### Timeline horizontale :

```
SEMAINES:  1    2    3    4    5    6  | 7    8    9   10   11   12   13   14
          ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
          │    PHASE 1 : ROS1         │        PHASE 2 : ROS2                   │
          ├───────────────────────────┼─────────────────────────────────────────┤

P1 (Nav)  [███ LIDAR ███][█ SLAM █][█ NAV █][█ MIG █][█ SLAM2 █][█ NAV2 █][TEST]
P2 (Vis)  [███ CAM8 ████][█ RGBD █][█ CV ██][█ MIG █][█ VIS2 ██][█ FINAL █][TEST]
P3 (Bras) [███ ARD █████][█ SER ██][█ UI ██][█ uROS █][█ RCLPY █][█ URDF ██][TEST]
P4 (Int)  [██ DOCK █████][█ ODOM █][█ INT █][█ ARCH █][█ ODOM2 █][█ LAUNCH█][TEST]
          
          └─ Setup ─┘└─ Intégr ┘└Final┘└─ Arch ─┘└─ Migr ──┘└─ Nav ──┘└Tests┘
                                  DEMO                                    DEMO
```

---

## 🎯 JALONS (MILESTONES)

| Jalon | Semaine | Description | Critères de validation |
|-------|---------|-------------|------------------------|
| **M1** | S2 | Environnement fonctionnel | Docker OK, tous les composants détectés |
| **M2** | S4 | Composants intégrés | LIDAR + Caméra + Arduino + Moteurs OK |
| **M3** | S6 | **🎉 ROBOT ROS1 OPÉRATIONNEL** | Navigation autonome démontrée |
| **M4** | S8 | Architecture ROS2 prête | Tous les packages ROS2 compilent |
| **M5** | S10 | Fonctions migrées | SLAM + Vision + Bras fonctionnels en ROS2 |
| **M6** | S12 | Navigation ROS2 | Robot navigue en ROS2 |
| **M7** | S14 | **🏆 PROJET TERMINÉ** | Démonstration complète ROS2 |

---

## 📊 CHARGE DE TRAVAIL PAR PERSONNE

### Répartition équilibrée sur 14 semaines :

| Personne | Semaines actives | Tâches principales | Charge |
|----------|------------------|-------------------|--------|
| **Personne 1** | S1-S14 | 7 tâches majeures | 100% |
| **Personne 2** | S1-S14 | 7 tâches majeures | 100% |
| **Personne 3** | S1-S14 | 7 tâches majeures | 100% |
| **Personne 4** | S1-S14 | 8 tâches majeures | 110% (+ intégration) |

**Note :** Personne 4 a plus de tâches car responsable de l'intégration globale.

---

## 🔗 DÉPENDANCES CRITIQUES

### Chemin critique (Critical Path) :

```
1.1 (Docker) → 1.2 (Compilation) → 1.3 (LIDAR) → 2.1 (SLAM) → 3.1 (Navigation) 
→ 3.5 (Demo ROS1) → 4.1 (Migration LIDAR) → 5.1 (SLAM2) → 6.1 (Navigation ROS2) 
→ 7.4 (Tests) → 7.6 (Demo finale)
```

**⚠️ Retard sur le chemin critique = retard sur tout le projet !**

---

## 📝 UTILISATION AVEC LOGICIELS GANTT

### Pour Microsoft Project / GanttProject / Asana :

1. **Copier** le tableau CSV ci-dessus
2. **Importer** dans votre logiciel
3. **Ajuster** les dates de début (ex : S1 = 01/11/2025)
4. **Ajouter** les dépendances entre tâches
5. **Assigner** les ressources (Personne 1-4)
6. **Générer** le diagramme

### Pour un Gantt rapide en ligne :
- **TeamGantt** : https://www.teamgantt.com/
- **Notion** : Créer une database avec timeline
- **Excel** : Utiliser un template Gantt
- **Google Sheets** : Template Gantt gratuit

---

## 🎨 CODES COULEUR RECOMMANDÉS

| Phase / Type | Couleur | Code Hex |
|--------------|---------|----------|
| Setup (S1-S2) | Bleu | #3498db |
| Intégration (S3-S4) | Vert | #2ecc71 |
| Navigation (S5-S6) | Orange | #f39c12 |
| Demo ROS1 | Rouge | #e74c3c |
| Architecture ROS2 (S7-S8) | Violet | #9b59b6 |
| Migration (S9-S10) | Turquoise | #1abc9c |
| Navigation ROS2 (S11-S12) | Gris foncé | #34495e |
| Tests (S13-S14) | Vert foncé | #16a085 |
| Demo finale | Rouge foncé | #c0392b |

---

## 📅 EXEMPLE DE DATES RÉELLES

Si vous commencez le **1er novembre 2025** :

| Semaine | Dates | Phase | Focus |
|---------|-------|-------|-------|
| S1 | 01/11 - 07/11 | Phase 1 | Setup + Tests LIDAR |
| S2 | 08/11 - 14/11 | Phase 1 | Tests composants |
| S3 | 15/11 - 21/11 | Phase 1 | SLAM + RGBD |
| S4 | 22/11 - 28/11 | Phase 1 | Odométrie |
| S5 | 29/11 - 05/12 | Phase 1 | Navigation |
| S6 | 06/12 - 12/12 | Phase 1 | **DEMO ROS1** 🎉 |
| S7 | 13/12 - 19/12 | Phase 2 | Architecture ROS2 |
| S8 | 20/12 - 26/12 | Phase 2 | Migration LIDAR/Cam |
| S9 | 27/12 - 02/01 | Phase 2 | ⚠️ Vacances possibles |
| S10 | 03/01 - 09/01 | Phase 2 | SLAM Toolbox |
| S11 | 10/01 - 16/01 | Phase 2 | Navigation ROS2 |
| S12 | 17/01 - 23/01 | Phase 2 | Launch files |
| S13 | 24/01 - 30/01 | Phase 2 | Tests |
| S14 | 31/01 - 06/02 | Phase 2 | **DEMO FINALE** 🏆 |

---

## 📊 RÉSUMÉ POUR GANTT EN 1 IMAGE

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PROJET ROBOCUP - 14 SEMAINES                     │
├─────────────────────────────────────────────────────────────────────┤
│ PHASE 1 (S1-S6) : ROS1                                              │
│   ├─ S1-S2 : Setup et tests (Docker, LIDAR, Caméras, Arduino)      │
│   ├─ S3-S4 : Intégration (SLAM, RGBD, ROS Serial, Odométrie)       │
│   └─ S5-S6 : Navigation autonome → DÉMONSTRATION                    │
├─────────────────────────────────────────────────────────────────────┤
│ PHASE 2 (S7-S14) : MIGRATION ROS2                                   │
│   ├─ S7-S8 : Architecture ROS2 et migration de base                │
│   ├─ S9-S10 : Migration fonctionnalités (SLAM Toolbox, vision)     │
│   ├─ S11-S12 : Navigation ROS2 et launch files                     │
│   └─ S13-S14 : Tests, optimisation → DÉMONSTRATION FINALE          │
└─────────────────────────────────────────────────────────────────────┘
```

---

**💡 Conseil :** Imprimez ce Gantt et accrochez-le dans votre salle de travail pour suivre la progression ! 📌
## 📚 RESSOURCES UTILES

### Tutoriels ROS1
- http://wiki.ros.org/ROS/Tutorials
- http://wiki.ros.org/navigation
- http://wiki.ros.org/hector_slam

### Tutoriels ROS2
- https://docs.ros.org/en/humble/Tutorials.html
- https://navigation.ros.org/
- https://github.com/ros2/examples

### Migration ROS1 → ROS2
- https://docs.ros.org/en/humble/How-To-Guides/Migrating-from-ROS1.html
- https://industrial-training-master.readthedocs.io/

---