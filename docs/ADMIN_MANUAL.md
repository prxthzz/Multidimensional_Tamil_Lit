# Administrator Manual

## 1. Administrative Overview
Administrators manage system configurations, roles, evidence approvals, and reproducible evaluation benchmarks.

## 2. Default Administrative Accounts
- **Super Admin**: `superadmin` / `Admin@123456`
- **System Admin**: `admin` / `Admin@123456`
- **Domain Expert**: `dr_sci_expert` / `Expert@123456`
- **Literary Expert**: `dr_tamil_expert` / `Expert@123456`
- **Security Auditor**: `auditor_1` / `Audit@123456`

## 3. Running Evaluation Benchmarks
```bash
python -c "import sys; sys.path.extend(['.', 'src']); import scripts.evaluate_system; scripts.evaluate_system.evaluate_ablation()"
```
