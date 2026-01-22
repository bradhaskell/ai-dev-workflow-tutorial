# Tasks: E-Commerce Sales Dashboard

**Input**: Design documents from `/specs/001-sales-dashboard/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: No automated tests requested. Manual browser testing per quickstart.md.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `app.py` at repository root (per plan.md)
- Data file: `data/sales-data.csv`
- Dependencies: `requirements.txt`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and dependency configuration

- [x] T001 Create requirements.txt with streamlit, pandas, and plotly dependencies at repository root
- [x] T002 Create .gitignore with venv/, __pycache__/, .streamlit/ exclusions at repository root
- [x] T003 Create app.py with basic Streamlit page configuration (title, layout) at repository root

**Checkpoint**: Project structure ready, can run `streamlit run app.py` with empty page

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data loading infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement load_data() function with @st.cache_data decorator in app.py
- [x] T005 Add date parsing with pd.to_datetime() in load_data() function in app.py
- [x] T006 Add error handling for missing CSV file with st.error() message in app.py
- [x] T007 Add error handling for empty CSV file with st.warning() message in app.py

**Checkpoint**: Foundation ready - `load_data()` returns valid DataFrame; user story implementation can now begin

---

## Phase 3: User Story 1 - View Key Performance Indicators (Priority: P1) 🎯 MVP

**Goal**: Display Total Sales and Total Orders as prominent KPI cards at the top of the dashboard

**Independent Test**: Load dashboard in browser, verify KPIs show Total Sales (~$650K-$700K with currency formatting) and Total Orders (482 with separators)

### Implementation for User Story 1

- [ ] T008 [US1] Create calculate_total_sales() function returning sum of total_amount in app.py
- [ ] T009 [US1] Create calculate_total_orders() function returning count of unique order_id in app.py
- [ ] T010 [US1] Create format_currency() helper function for $X,XXX,XXX formatting in app.py
- [ ] T011 [US1] Create format_number() helper function for thousand separators in app.py
- [ ] T012 [US1] Add KPI display section using st.columns() and st.metric() in app.py
- [ ] T013 [US1] Add dashboard title "ShopSmart Sales Dashboard" using st.title() in app.py

**Checkpoint**: User Story 1 complete - KPIs display correctly with formatted values

---

## Phase 4: User Story 2 - Analyze Sales Trends Over Time (Priority: P2)

**Goal**: Display a line chart showing monthly sales trends with interactive tooltips

**Independent Test**: Load dashboard, verify line chart shows 12 months of data chronologically with tooltips on hover

### Implementation for User Story 2

- [ ] T014 [US2] Create aggregate_monthly_sales() function using groupby on date month in app.py
- [ ] T015 [US2] Create create_trend_chart() function using plotly express line chart in app.py
- [ ] T016 [US2] Configure chart with title "Sales Trend Over Time", axis labels in app.py
- [ ] T017 [US2] Configure interactive tooltips showing date and sales value in app.py
- [ ] T018 [US2] Add trend chart to dashboard layout using st.plotly_chart() with use_container_width=True in app.py

**Checkpoint**: User Story 2 complete - Line chart displays monthly trends with interactivity

---

## Phase 5: User Story 3 - Compare Sales by Product Category (Priority: P3)

**Goal**: Display a bar chart showing sales by category, sorted highest to lowest

**Independent Test**: Load dashboard, verify bar chart shows all 5 categories (Electronics, Accessories, Audio, Wearables, Smart Home) sorted by value with tooltips

### Implementation for User Story 3

- [ ] T019 [US3] Create aggregate_category_sales() function using groupby on category in app.py
- [ ] T020 [US3] Create create_category_chart() function using plotly express bar chart in app.py
- [ ] T021 [US3] Configure chart with title "Sales by Category", sorted descending in app.py
- [ ] T022 [US3] Configure interactive tooltips showing category and sales value in app.py
- [ ] T023 [US3] Add category chart to dashboard layout using st.plotly_chart() in app.py

**Checkpoint**: User Story 3 complete - Category bar chart displays all 5 categories sorted by value

---

## Phase 6: User Story 4 - Compare Sales by Geographic Region (Priority: P4)

**Goal**: Display a bar chart showing sales by region, sorted highest to lowest

**Independent Test**: Load dashboard, verify bar chart shows all 4 regions (North, South, East, West) sorted by value with tooltips

### Implementation for User Story 4

- [ ] T024 [US4] Create aggregate_region_sales() function using groupby on region in app.py
- [ ] T025 [US4] Create create_region_chart() function using plotly express bar chart in app.py
- [ ] T026 [US4] Configure chart with title "Sales by Region", sorted descending in app.py
- [ ] T027 [US4] Configure interactive tooltips showing region and sales value in app.py
- [ ] T028 [US4] Add region chart to dashboard layout using st.plotly_chart() in app.py

**Checkpoint**: User Story 4 complete - Region bar chart displays all 4 regions sorted by value

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and validation

- [ ] T029 Arrange category and region charts side-by-side using st.columns() in app.py
- [ ] T030 Add professional styling with consistent color scheme across all charts in app.py
- [ ] T031 Verify all charts have clear axis labels and titles in app.py
- [ ] T032 Run quickstart.md validation checklist to verify all acceptance criteria
- [ ] T033 Test dashboard in multiple browsers (Chrome, Firefox, Edge)

**Checkpoint**: Dashboard complete and validated against all acceptance criteria

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (data loading)
    ↓
┌───────────────────────────────────────────────┐
│  User Stories can proceed in priority order:  │
│  Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3) → Phase 6 (US4)  │
│  OR in parallel if multiple developers        │
└───────────────────────────────────────────────┘
    ↓
Phase 7: Polish
```

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Phase 2 (load_data). No dependencies on other stories.
- **User Story 2 (P2)**: Depends on Phase 2 (load_data). Independent of US1.
- **User Story 3 (P3)**: Depends on Phase 2 (load_data). Independent of US1/US2.
- **User Story 4 (P4)**: Depends on Phase 2 (load_data). Independent of US1/US2/US3.

### Within Each User Story

1. Aggregation function first (calculates data)
2. Chart creation function second (builds visualization)
3. Layout integration last (adds to dashboard)

### Parallel Opportunities

Since all user stories modify the same file (`app.py`), parallel execution requires coordination. However, functions can be developed independently:

```bash
# US3 and US4 can be developed in parallel (different functions):
# Developer A: aggregate_category_sales(), create_category_chart()
# Developer B: aggregate_region_sales(), create_region_chart()
# Merge both into app.py layout section
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T007)
3. Complete Phase 3: User Story 1 (T008-T013)
4. **STOP and VALIDATE**: Dashboard shows KPIs correctly
5. Can deploy MVP to Streamlit Cloud with just KPIs

### Incremental Delivery

1. Setup + Foundational → Data loading works
2. Add User Story 1 → KPIs display (MVP!)
3. Add User Story 2 → Trend chart appears
4. Add User Story 3 → Category breakdown added
5. Add User Story 4 → Regional breakdown completes dashboard
6. Polish → Professional appearance finalized

### Single Developer Strategy

Execute tasks sequentially in order (T001 → T033). Each phase builds on previous.

---

## Notes

- All tasks modify `app.py` - single file application per constitution
- No [P] markers on user story tasks since they share the same file
- Each user story is independently testable once foundational phase complete
- Commit after each phase completion with Jira reference (ECOM-X)
- Run `streamlit run app.py` after each checkpoint to verify progress
