# Advance Payment Status Reference

This document records the status values currently used by the advance-payment
module. Values are documented exactly as stored today, including Thai labels and
legacy values. It is intended as the baseline for a later integer-status
migration.

## Verified database inventory

The following was queried from the configured PostgreSQL database on 2026-10-27.
Counts are current rows, not the complete set of values supported by the code.

| Table | Stored status | Row count |
|---|---|---:|
| `cash_advance_borrowing_tickets` | `กำลังส่งคำขอ` | 1 |
| `cash_advance_borrowing_tickets` | `เคลียร์ยอดแล้ว` | 4 |
| `cash_advance_borrowing_tickets` | `ปฏิเสธ` | 3 |
| `cash_advance_borrowing_tickets` | `มียอดคงค้าง` | 1 |
| `cash_advance_borrowing_tickets` | `อนุมัติจ่ายเงิน` | 1 |
| `cash_advance_return_details` | `ผ่านการตรวจสอบ` | 5 |
| `cash_advance_return_details` | `รอตรวจสอบ` | 1 |
| `cash_advance_return_details` | `ล้างลูกหนี้เงินยืม` | 1 |
| `cash_mng_parcel_return_details` | `ได้รับเอกสารแล้ว` | 1 |
| `cash_mng_parcel_return_details` | `ยืนยันการตรวจสอบ` | 1 |
| `cash_mng_parcel_return_details` | `ล้างลูกหนี้เงินยืม` | 2 |
| `cash_mng_parcel_return_details` | `เอกสารตั้งฎีกา` | 2 |
| `cash_mng_parcel_return_details` | `โอนเงินสดย่อยสำเร็จ` | 2 |
| `petty_cash_claim_details` | `ผ่านการตรวจสอบ` | 1 |
| `petty_cash_claim_details` | `รอตรวจสอบ` | 2 |
| `petty_cash_claim_details` | `เสร็จสิ้นกระบวนการ` | 1 |
| `petty_cash_claim_details` | `โอนคืนเงินสดย่อย` | 2 |
| `petty_cash_claim_details` | `โอนเงินสดย่อยสำเร็จ` | 3 |
| `petty_cash_fund_requests` | `เคลียร์ยอดสำเร็จ` | 1 |
| `petty_cash_fund_requests` | `เบิกเงินแล้ว` | 9 |
| `petty_cash_fund_requests` | `รอการอนุมัติ` | 2 |
| `petty_cash_fund_requests` | `ส่งเบิกครบแล้ว` | 2 |
| `petty_cash_fund_requests` | `อนุมัติแล้ว` | 1 |

The code supports `ฎีกาถูกตีกลับจากกองคลัง` for both borrowing tickets and
return details, but no current database row has that value.

## Assigned status IDs

These business codes are seeded by migration
`s2t3u4v5w6x7_seed_advance_payment_statuses.py`. The first digit identifies the
workflow system; the last two digits identify the status order within that
system. The database `id` is a separate auto-generated primary key.

The five status-bearing tables reference this catalog through `status_id`:

| Table | Status group | Reference column |
|---|---|---|
| `cash_advance_borrowing_tickets` | `borrowing_ticket` | `status_id` |
| `cash_advance_return_details` | `return_detail` | `status_id` |
| `cash_mng_parcel_return_details` | `parcel_return` | `status_id` |
| `petty_cash_fund_requests` | `fund_request` | `status_id` |
| `petty_cash_claim_details` | `petty_cash_claim` | `status_id` |

The existing text `status` columns remain temporarily so the current workflow
can be migrated incrementally. The linking migration backfills `status_id` by
matching the existing text status and the table's status group.

| System digit | Status group | System |
|---:|---|---|
| 1 | `borrowing_ticket` | Borrowing ticket |
| 2 | `return_detail` | Return detail |
| 3 | `parcel_return` | Parcel return |
| 4 | `fund_request` | Fund request |
| 5 | `petty_cash_claim` | Petty-cash claim |

| id | **Status group** | **Code** | **Name** |
|---|---|---:|---|
| — | `borrowing_ticket` | 101 | กำลังส่งคำขอ |
| — | `borrowing_ticket` | 102 | กำลังดำเนินการ |
| — | `borrowing_ticket` | 103 | อนุมัติแล้ว |
| — | `borrowing_ticket` | 104 | อนุมัติจ่ายเงิน |
| — | `borrowing_ticket` | 105 | มียอดคงค้าง |
| — | `borrowing_ticket` | 106 | เอกสารตั้งฎีกา |
| — | `borrowing_ticket` | 107 | ฎีกาถูกตีกลับจากกองคลัง |
| — | `borrowing_ticket` | 108 | เคลียร์ยอดแล้ว |
| — | `borrowing_ticket` | 109 | ปฏิเสธ |
| — | `return_detail` | 201 | ฉบับร่าง |
| — | `return_detail` | 202 | รอตรวจสอบ |
| — | `return_detail` | 203 | กำลังตรวจสอบ |
| — | `return_detail` | 204 | ผ่านการตรวจสอบ |
| — | `return_detail` | 205 | ปฏิเสธ |
| — | `return_detail` | 206 | รอยืนยันการแก้ไข |
| — | `return_detail` | 207 | ฎีกาถูกตีกลับจากกองคลัง |
| — | `parcel_return` | 301 | ฉบับร่าง |
| — | `parcel_return` | 302 | รอตรวจสอบ |
| — | `parcel_return` | 303 | กำลังตรวจสอบ |
| — | `parcel_return` | 304 | ผ่านการตรวจสอบ |
| — | `parcel_return` | 305 | ปฏิเสธ |
| — | `parcel_return` | 306 | ถูกปฏิเสธ |
| — | `parcel_return` | 307 | รอยืนยันการแก้ไข |
| — | `parcel_return` | 308 | พัสดุกำลังดำเนินการ |
| — | `parcel_return` | 309 | ได้รับเอกสารแล้ว |
| — | `parcel_return` | 310 | ยืนยันการตรวจสอบ |
| — | `parcel_return` | 311 | โอนเงินสดย่อยสำเร็จ |
| — | `fund_request` | 401 | รอการอนุมัติ |
| — | `fund_request` | 402 | อนุมัติแล้ว |
| — | `fund_request` | 403 | เบิกเงินแล้ว |
| — | `fund_request` | 404 | ส่งเบิกครบแล้ว |
| — | `fund_request` | 405 | เคลียร์ยอดสำเร็จ |
| — | `fund_request` | 406 | ยกเลิก |
| — | `fund_request` | 407 | ยกเลิกใบเบิก |
| — | `fund_request` | 408 | ฉบับร่าง |
| — | `petty_cash_claim` | 501 | ฉบับร่าง |
| — | `petty_cash_claim` | 502 | รอตรวจสอบ |
| — | `petty_cash_claim` | 503 | กำลังตรวจสอบ |
| — | `petty_cash_claim` | 504 | ผ่านการตรวจสอบ |
| — | `petty_cash_claim` | 505 | ปฏิเสธ |
| — | `petty_cash_claim` | 506 | ถูกปฏิเสธ |
| — | `petty_cash_claim` | 507 | รอยืนยันการแก้ไข |
| — | `petty_cash_claim` | 508 | โอนคืนเงินสดย่อย |
| — | `petty_cash_claim` | 509 | โอนเงินสดย่อยสำเร็จ |
| — | `petty_cash_claim` | 510 | เสร็จสิ้นกระบวนการ |
| — | `petty_cash_claim` | 511 | ยกเลิก |

## Status-bearing tables

### `cash_advance_borrowing_tickets`

Model: `CashAdvanceBorrowingTicket` / `BorrowingTicket`

| Current value | Meaning / workflow role |
|---|---|
| `กำลังส่งคำขอ` | Request is being submitted. Model default. |
| `กำลังดำเนินการ` | Request is in progress. |
| `อนุมัติแล้ว` | Request approved. |
| `อนุมัติจ่ายเงิน` | Payment approval recorded. |
| `มียอดคงค้าง` | Outstanding balance remains. |
| `เอกสารตั้งฎีกา` | Closing/payment document has been prepared. |
| `ฎีกาถูกตีกลับจากกองคลัง` | Closing document was returned by the treasury. |
| `เคลียร์ยอดแล้ว` | Balance has been cleared. |
| `ปฏิเสธ` | Request rejected. |
| `ยกเลิก` | Request cancelled. |

### `cash_advance_return_details`

Model: `ReturnDetail`

| Current value | Meaning / workflow role |
|---|---|
| `รอตรวจสอบ` | Waiting for finance review. Model default. |
| `กำลังตรวจสอบ` | Finance review is in progress. |
| `ผ่านการตรวจสอบ` | Review passed. |
| `ปฏิเสธ` | Return detail rejected. |
| `รอยืนยันการแก้ไข` | Waiting for the requester to confirm/edit. |
| `ฎีกาถูกตีกลับจากกองคลัง` | Closing document was returned by the treasury. |
| `ฉบับร่าง` | Draft/legacy value used by some paths. |

### `cash_mng_parcel_return_details`

Model: `ParcelReturnDetail`

| Current value | Meaning / workflow role |
|---|---|
| `รอตรวจสอบ` | Waiting for document/finance review. Model default. |
| `ฉบับร่าง` | Draft parcel-return record saved before submission. Supported by the parcel-return workflow. |
| `กำลังตรวจสอบ` | Review is in progress. |
| `ผ่านการตรวจสอบ` | Review passed. |
| `ปฏิเสธ` / `ถูกปฏิเสธ` | Parcel return rejected; both spellings are supported. |
| `รอยืนยันการแก้ไข` | Waiting for requester correction. |
| `พัสดุกำลังดำเนินการ` | Parcel process is underway. |
| `ได้รับเอกสารแล้ว` | Supporting document received. |
| `ยืนยันการตรวจสอบ` | Confirmation status for selected parcel-return types. |
| `โอนเงินสดย่อยสำเร็จ` | Petty-cash transfer completed. |
| `เอกสารตั้งฎีกา` | Closing/payment document prepared. |
| `ล้างลูกหนี้เงินยืม` | Borrower balance cleared. |

### `petty_cash_fund_requests`

Model: `FundRequest`

| Current value | Meaning / workflow role |
|---|---|
| `รอการอนุมัติ` | Waiting for required approval. Model default. |
| `อนุมัติแล้ว` | Fully approved. |
| `เบิกเงินแล้ว` | Money disbursed. |
| `ส่งเบิกครบแล้ว` | All related claims/returns submitted. |
| `เคลียร์ยอดสำเร็จ` | Fund request fully settled. |
| `ยกเลิก` | Cancelled before/around processing. |
| `ยกเลิกใบเบิก` | Claim/request cancellation recorded as a cancelled document. |

### `petty_cash_claim_details`

Model: `PettyCashClaimDetail`

| Current value | Meaning / workflow role |
|---|---|
| `ฉบับร่าง` | Draft. Model default. |
| `รอตรวจสอบ` | Waiting for finance review. |
| `กำลังตรวจสอบ` | Review is in progress. |
| `ผ่านการตรวจสอบ` | Review passed. |
| `ปฏิเสธ` / `ถูกปฏิเสธ` | Claim rejected; both values are supported. |
| `รอยืนยันการแก้ไข` | Waiting for requester correction/confirmation. |
| `โอนคืนเงินสดย่อย` | Cash returned to petty cash. |
| `โอนเงินสดย่อยสำเร็จ` | Petty-cash transfer completed. |
| `เสร็จสิ้นกระบวนการ` | Claim workflow completed. |
| `ยกเลิก` | Claim cancelled. |
| `ใบเบิกถูกปฏิเสธ` | Legacy rejected-claim value. |

## Tables without a persisted status column

The following advance-payment tables were checked and do not currently define a
`status` column: notifications, documents, receipt items, proof files, closing
documents, closing-document links, petty-cash settings, fiscal-year transfers,
finance state, fiscal-year carryovers, bank account information, account
managers, fund-request items, claim items, and claim proof files.

## Migration notes

- Status values are currently stored as text, so spelling and whitespace matter.
- Some workflows intentionally support legacy duplicates such as `ปฏิเสธ` and
  `ถูกปฏิเสธ`.
- `FundRequest` has a five-step main workflow, but also uses cancellation values.
- Before converting a table to integer IDs, normalize duplicate/legacy values
  and decide whether each status is shared across tables or table-specific.
- The next migration should preserve this document as the mapping source and
  update model defaults, view comparisons, templates, and existing rows in one
  transaction per table.
