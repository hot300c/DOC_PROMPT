using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Linq;
using System.Text;
using Aladdin.Entities;
using Aladdin.Services;
using Aladdin.Utilities;
using LinqToDB;
using LinqToDB.DataProvider.SqlServer;

namespace Aladdin.WebService.Handlers.QAHosGenericDB;

// ReSharper disable once InconsistentNaming
public class ws_QuanLyTapTrung(
AladdinDataConnection db,
DateTimeService dateTimeService,
MasterDataService masterDataService,
SettingsService settingsService
) : GenericHandler<ws_QuanLyTapTrung.Parameters>
{
// Tương ứng với file backup lines 38-102: DTO Classes
private class FacAdmissionDto
{
public Guid FacAdmissionId { get; init; } // SP: FacAdmissionId
public int? NguonTiepNhan { get; init; } // SP: NguonTiepNhan
public Guid? PatientId { get; init; } // SP: PatientId
public string? FacId { get; init; } // SP: FacId
public Guid? CreatedBy { get; init; } // SP: CreatedBy
public DateTime? DischargedOn { get; init; } // SP: DischargedOn
public DateTime? AdmitDate { get; init; } // SP: AdmitDate
public int? AdmitDateAsInt { get; init; } // SP: AdmitDateAsInt
public DateTime? AdmitOn { get; init; } // SP: AdmitOn
public int? TuoiAsInt { get; init; } // SP: TuoiAsInt (tính từ DoB)
public bool? IsChieu { get; init; } // SP: IsChieu
}

    private class ClinicalSessionDto
    {
        public Guid ClinicalSessionId { get; set; } // SP: ClinicalSessionId
        public Guid? FacAdmissionId { get; set; } // SP: FacAdmissionId
        public Guid? PhysicianAdmissionId { get; set; } // SP: PhysicianAdmissionId
        public Guid? PatientId { get; set; } // SP: PatientId
        public int? ServiceId { get; set; } // SP: ServiceId
        public Guid? HopDongId { get; set; } // SP: HopDongId
        public DateTime? CompletedOn { get; set; } // SP: CompletedOn
        public int? ProductTypeId { get; set; } // SP: ProductTypeId
        public bool? IsDuocTiem { get; set; } // SP: IsDuocTiem
        public int? RoomId { get; set; } // SP: RoomId
        public int? ServiceTypeId { get; set; } // SP: ServiceTypeId
        public string? FacId { get; set; } // SP: FacId
    }

    private class PhysicianAdmissionDto
    {
        public Guid PhysicianAdmissionId { get; set; } // SP: PhysicianAdmissionId
        public DateTime? DischargedOn { get; set; } // SP: DischargedOn
        public bool? IsKhongDuocTiem { get; set; } // SP: IsKhongDuocTiem
        public Guid? PatientId { get; set; } // SP: PatientId
        public Guid? PrimaryDoctor { get; set; } // SP: PrimaryDoctor
        public int? RoomId { get; set; } // SP: RoomId
        public Guid? FacAdmissionId { get; set; } // SP: FacAdmissionId
        public DateTime? AdmitDate { get; set; } // SP: AdmitDate
        public string? FacId { get; set; } // SP: FacId
        public DateTime? TgBatDauKham { get; set; } // SP: TgBatDauKham
        public bool? IsPracticed { get; set; } // SP: IsPracticed
    }

    public class Parameters
    {
        public string? SessionId { get; set; }
        public DateTime TuNgay { get; set; }
        public DateTime DenNgay { get; set; }
        public string FacId { get; set; }

        [DisplayName("_Type")]
        public int Type { get; set; } = 0;

        public int Debug { get; set; } = 0;
    }

    public override DataSet Handle(Parameters @params)
    {
        var dataSet = new DataSet();

        // Convert dates to required formats
        var tuNgayAsInt = @params.TuNgay.DateAsInt();
        var denNgayAsInt = @params.DenNgay.DateAsInt();
        var tuNgayAsBigInt = tuNgayAsInt * 1_000_000L;
        var denNgayAsBigInt = denNgayAsInt * 1_000_000L + 235959;
        var checksumFacId = DataUtils.Checksum(@params.FacId);

        // Handle different report types
        switch (@params.Type)
        {
            case 1: // Tổng quan
                return HandleTongQuan(@params, tuNgayAsInt, denNgayAsInt, tuNgayAsBigInt, denNgayAsBigInt, checksumFacId);
            case 2: // Chi tiết tiếp nhận
                return HandleChiTietTiepNhan(@params, tuNgayAsInt, denNgayAsInt, checksumFacId);
            case 3: // Chi tiết tiếp nhận theo địa lý
                return HandleChiTietTiepNhanDiaLy(@params, tuNgayAsInt, denNgayAsInt, checksumFacId);
            case 4: // Chi tiết doanh thu
                return HandleChiTietDoanhThu(@params, tuNgayAsBigInt, denNgayAsBigInt, checksumFacId);
            case 5: // Chi tiết khám bệnh
                return HandleChiTietKhamBenh(@params, tuNgayAsInt, denNgayAsInt, checksumFacId);
            case 6: // Chi tiết phòng tiêm
                return HandleChiTietPhongTiem(@params, tuNgayAsInt, denNgayAsInt, checksumFacId);
            case 7: // Chi tiết thời gian
                return HandleChiTietThoiGian(@params, tuNgayAsInt, denNgayAsInt, checksumFacId);
            case 8: // Chi tiết đặt trước
                return HandleChiTietDatTruoc(@params, tuNgayAsInt, denNgayAsInt, checksumFacId);
            case 9: // Chi tiết không được tiêm
                return HandleChiTietKhongDuocTiem(@params, tuNgayAsInt, denNgayAsInt, checksumFacId);
            case 10: // Chi tiết xuất kho vaccine
                return HandleChiTietXuatKhoVaccine(@params, tuNgayAsInt, denNgayAsInt, checksumFacId);
            case 1111: // Bệnh nhân có nhiều công khám
                return HandleBenhNhanNhieuCongKham(@params, tuNgayAsInt, denNgayAsInt, checksumFacId);
            default:
                throw new ArgumentException($"Không hỗ trợ loại báo cáo: {@params.Type}");
        }
    }

    private DataSet HandleTongQuan(
        Parameters @params,
        int tuNgayAsInt,
        int denNgayAsInt,
        long tuNgayAsBigInt,
        long denNgayAsBigInt,
        int checksumFacId
    )
    {
        var dataSet = new DataSet();

        // Tương ứng file backup lines 115-280: Lấy dữ liệu cơ bản
        var facAdmissions = GetFacAdmissionsWithTuoi(@params, tuNgayAsInt, denNgayAsInt);
        var clinicalSessions = GetClinicalSessions(@params, tuNgayAsInt, denNgayAsInt);
        var clinicalSessionsVaccine = GetClinicalSessionsVaccine(@params, tuNgayAsInt, denNgayAsInt, checksumFacId);
        var physicianAdmissions = GetPhysicianAdmissions(@params, tuNgayAsInt, denNgayAsInt);

        // Tương ứng file backup lines 280-400: Tính toán chi tiết
        var detailedStats = CalculateDetailedStatistics(
            @params,
            tuNgayAsInt,
            denNgayAsInt,
            tuNgayAsBigInt,
            denNgayAsBigInt,
            checksumFacId,
            facAdmissions,
            clinicalSessions,
            clinicalSessionsVaccine,
            physicianAdmissions
        );

        // Tương ứng file backup lines 400-600: Tính toán doanh thu
        var bilInvoiceDetails = GetBilInvoiceDetails(@params, tuNgayAsBigInt, denNgayAsBigInt, checksumFacId);
        var detailedRevenue = CalculateDetailedRevenue(
            @params,
            tuNgayAsInt,
            denNgayAsInt,
            tuNgayAsBigInt,
            denNgayAsBigInt,
            checksumFacId,
            bilInvoiceDetails
        );

        // Tương ứng file backup lines 600-800: Tính toán các chỉ số khác
        var otherStats = CalculateOtherStatistics(@params, tuNgayAsInt, denNgayAsInt, facAdmissions, clinicalSessions);

        // Tương ứng file backup lines 800-1000: Tạo bảng kết quả
        var tempTongQuan = CreateTongQuanTable(detailedStats, detailedRevenue, otherStats);

        // Table0: Bảng tổng quan chính
        dataSet.Tables.Add(tempTongQuan);

        // Table1: Thống kê tiêm chủng
        dataSet.Tables.Add(CreateTiemChungTable(detailedStats));

        // Table2: Thống kê khách được/không được tiêm
        dataSet.Tables.Add(CreateKhachTiemTable(detailedStats));

        // Table3: Số bệnh nhân hôm nay
        dataSet.Tables.Add(CreateBenhNhanHomNayTable(@params));

        // Table4: Báo cáo văn bản
        dataSet.Tables.Add(CreateBaoCaoVanBanTable(@params, detailedStats, detailedRevenue, otherStats));

        return dataSet;
    }

    // Tương ứng với file backup lines 115-280: Data Retrieval Functions
    private List<FacAdmissionDto> GetFacAdmissionsWithTuoi(Parameters @params, int tuNgayAsInt, int denNgayAsInt)
    {
        var facAdmissionsQuery = db
            .QAHosGenericDB.CnFacAdmissions.With(SqlServerHints.Table.NoLock)
            .Where(a => a.FacId == @params.FacId && a.AdmitDateAsInt.Between(tuNgayAsInt, denNgayAsInt));

        var facAdmissionsWithTuoiQuery =
            from a in facAdmissionsQuery
            from p in db
                .QAHosGenericDB.MdmPatients.With(SqlServerHints.Table.NoLock)
                .LeftJoin(p => p.PatientId == a.PatientId)
            select new FacAdmissionDto
            {
                FacAdmissionId = a.FacAdmissionId,
                NguonTiepNhan = a.NguonTiepNhan,
                PatientId = a.PatientId,
                FacId = a.FacId,
                CreatedBy = a.CreatedBy,
                DischargedOn = a.DischargedOn,
                AdmitDate = a.AdmitDate,
                AdmitDateAsInt = a.AdmitDateAsInt,
                AdmitOn = a.AdmitOn,
                TuoiAsInt = SqlFn.DateDiff(SqlFn.DateParts.Year, p.DoB, a.AdmitOn),
                IsChieu = a.IsChieu,
            };

        return facAdmissionsWithTuoiQuery.ToList();
    }

    private List<ClinicalSessionDto> GetClinicalSessions(Parameters @params, int tuNgayAsInt, int denNgayAsInt)
    {
        return db
            .QAHosGenericDB.CnClinicalSessions.With(SqlServerHints.Table.NoLock)
            .Where(a => a.UserCreatedDateAsInt.Between(tuNgayAsInt, denNgayAsInt))
            .Select(cs => new ClinicalSessionDto
            {
                ClinicalSessionId = cs.ClinicalSessionId,
                FacAdmissionId = cs.FacAdmissionId,
                PhysicianAdmissionId = cs.PhysicianAdmissionId,
                PatientId = cs.PatientId,
                ServiceId = cs.ServiceId,
                HopDongId = cs.HopDongId,
                CompletedOn = cs.CompletedOn,
                ProductTypeId = cs.ProductTypeId,
                IsDuocTiem = cs.IsDuocTiem,
                RoomId = cs.RoomId,
                ServiceTypeId = cs.ServiceTypeId,
                FacId = cs.FacId,
            })
            .ToList();
    }

    private List<ClinicalSessionDto> GetClinicalSessionsVaccine(
        Parameters @params,
        int tuNgayAsInt,
        int denNgayAsInt,
        int checksumFacId
    )
    {
        var clinicalSessions = GetClinicalSessions(@params, tuNgayAsInt, denNgayAsInt);

        var clinicalSessionsVaccineQuery =
            from t in clinicalSessions
            from cs in db
                .QAHosGenericDB.CnClinicalSessionIdVaccines.With(SqlServerHints.Table.NoLock)
                .Where(cs => cs.ClinicalSessionId == t.ClinicalSessionId)
            where
                (cs.FacIdChiDinhChecksum == checksumFacId && cs.NgayChiDinhAsInt.Between(tuNgayAsInt, denNgayAsInt))
                || (cs.FacIdDaTiemChecksum == checksumFacId && cs.NgayTiemAsInt.Between(tuNgayAsInt, denNgayAsInt))
            select new ClinicalSessionDto
            {
                ClinicalSessionId = cs.ClinicalSessionId,
                PatientId = t.PatientId,
                CompletedOn = t.CompletedOn,
                ProductTypeId = t.ProductTypeId,
                IsDuocTiem = t.IsDuocTiem,
                PhysicianAdmissionId = t.PhysicianAdmissionId,
                FacId = t.FacId,
            };

        return clinicalSessionsVaccineQuery.ToList();
    }

    private List<PhysicianAdmissionDto> GetPhysicianAdmissions(Parameters @params, int tuNgayAsInt, int denNgayAsInt)
    {
        return db
            .QAHosGenericDB.CnPhysicianAdmissions.With(SqlServerHints.Table.NoLock)
            .Where(a =>
                a.FacId == @params.FacId && a.AdmitDateAsInt.Between(tuNgayAsInt, denNgayAsInt) && a.RoomId != 0
            )
            .Select(pa => new PhysicianAdmissionDto
            {
                PhysicianAdmissionId = pa.PhysicianAdmissionId,
                DischargedOn = pa.DischargedOn,
                IsKhongDuocTiem = pa.IsKhongDuocTiem,
                PatientId = pa.PatientId,
                PrimaryDoctor = pa.PrimaryDoctor,
                RoomId = pa.RoomId,
                FacAdmissionId = pa.FacAdmissionId,
                AdmitDate = pa.AdmitDate,
                FacId = pa.FacId,
                TgBatDauKham = pa.TgBatDauKham,
                IsPracticed = pa.IsPracticed,
            })
            .ToList();
    }

    // Tương ứng với file backup lines 280-400: CalculateDetailedStatistics
    private Dictionary<string, object> CalculateDetailedStatistics(
        Parameters @params,
        int tuNgayAsInt,
        int denNgayAsInt,
        long tuNgayAsBigInt,
        long denNgayAsBigInt,
        int checksumFacId,
        List<FacAdmissionDto> facAdmissions,
        List<ClinicalSessionDto> clinicalSessions,
        List<ClinicalSessionDto> clinicalSessionsVaccine,
        List<PhysicianAdmissionDto> physicianAdmissions
    )
    {
        var result = new Dictionary<string, object>();

        // Tính toán tiếp nhận theo nguồn
        var tiepNhanTheoNguon = new Dictionary<int, int>();
        for (int nguonTiepNhan = 1; nguonTiepNhan <= 7; nguonTiepNhan++)
        {
            int soLuong = facAdmissions
                .Where(a => a.NguonTiepNhan == nguonTiepNhan)
                .GroupBy(a => a.AdmitDate)
                .Select(g => g.Select(x => x.PatientId).Distinct().Count())
                .Sum();
            tiepNhanTheoNguon[nguonTiepNhan] = soLuong;
        }
        result["TiepNhanTheoNguon"] = tiepNhanTheoNguon;

        // Tính toán khách đặt trước
        var bilInvoiceDetails = GetBilInvoiceDetails(@params, tuNgayAsBigInt, denNgayAsBigInt, checksumFacId);
        var khachDatTruocs = bilInvoiceDetails
            .Where(t => t.Loai == "Đặt trước")
            .Select(t => t.PatientId)
            .ToHashSet();
        int soKhachDatTruoc = khachDatTruocs.Count;
        int soKhachDatTruocCoKham = facAdmissions
            .Where(a => khachDatTruocs.Contains(a.PatientId ?? Guid.Empty))
            .Select(a => a.PatientId)
            .Distinct()
            .Count();
        result["SoKhachDatTruoc"] = soKhachDatTruoc;
        result["SoKhachDatTruocCoKham"] = soKhachDatTruocCoKham;

        // Tính toán khách hợp đồng
        var khachHopDongs = GetKhachHopDongs(@params, tuNgayAsInt, denNgayAsInt);
        int soKhachHopDong = khachHopDongs.Count;
        int soKhachHopDongCoKham = facAdmissions
            .Where(a => khachHopDongs.Contains(a.PatientId))
            .DistinctBy(a => a.PatientId)
            .Count();
        result["SoKhachHopDong"] = soKhachHopDong;
        result["SoKhachHopDongCoKham"] = soKhachHopDongCoKham;

        // Tính toán khách mới
        int tongSoLuotTnMoi = db
            .QAHosGenericDB.MdmPatients.With(SqlServerHints.Table.NoLock)
            .Count(p => p.FacId == @params.FacId && p.CreatedItemAsInt.Between(tuNgayAsInt, denNgayAsInt));
        result["TongSoLuotTnMoi"] = tongSoLuotTnMoi;

        // Tính toán khách khám lẻ và hợp đồng
        int tongSoKhachKham = clinicalSessions
            .Where(c => c.HopDongId == null)
            .Select(c => c.PatientId)
            .Distinct()
            .Count();
        int tongSoKhachKhamHd = clinicalSessions
            .Where(c => c.HopDongId != null)
            .Select(c => c.PatientId)
            .Distinct()
            .Count();
        result["TongSoKhachKham"] = tongSoKhachKham;
        result["TongSoKhachKhamHd"] = tongSoKhachKhamHd;

        // Tính toán khách được/không được tiêm
        int tongSoKhachDuocTiem = clinicalSessionsVaccine.Select(t => t.PatientId).Distinct().Count();
        int tongKhachKhongDuocTiem = physicianAdmissions.Count(a =>
            a.IsKhongDuocTiem == true && a.DischargedOn != null
        );
        result["TongSoKhachDuocTiem"] = tongSoKhachDuocTiem;
        result["TongKhachKhongDuocTiem"] = tongKhachKhongDuocTiem;

        // Tính toán khách bỏ về
        int soLuotBoVe = (
            from a in facAdmissions
            from b in db
                .QAHosGenericDB.CnDoctorDecisions.With(SqlServerHints.Table.NoLock)
                .Where(b => b.FacAdmissionId == a.FacAdmissionId && b.FinalDecisionId != 1)
            select 1
        ).Count();
        result["SoLuotBoVe"] = soLuotBoVe;

        // Tính toán khách đã tiêm
        int tongSoKhachDaTiem = clinicalSessionsVaccine
            .Where(c => c.CompletedOn != null)
            .DistinctBy(c => c.PatientId)
            .Count();
        result["TongSoKhachDaTiem"] = tongSoKhachDaTiem;

        // Tính toán khách người lớn
        int tongSoNguoiLon = facAdmissions
            .Where(a => a.TuoiAsInt >= 18)
            .Select(a => new { a.PatientId, a.AdmitDateAsInt })
            .Distinct()
            .Count();
        result["TongSoNguoiLon"] = tongSoNguoiLon;

        // Tính toán khách khám người thân
        int tongSoKhamNguoiThan = (
            from b in clinicalSessions
            from c in physicianAdmissions.Where(c => c.PhysicianAdmissionId == b.PhysicianAdmissionId)
            where
                b.ServiceTypeId == 1
                && db.QAHosGenericDB.LDepartmentRooms.With(SqlServerHints.Table.NoLock)
                    .Any(d => d.RoomId == b.RoomId && d.RoomName.Contains("Người thân") && d.FacId == @params.FacId)
            select b.PatientId
        )
            .Distinct()
            .Count();
        result["TongSoKhamNguoiThan"] = tongSoKhamNguoiThan;

        return result;
    }

    // Tương ứng với file backup lines 400-600: CalculateDetailedRevenue
    private Dictionary<string, object> CalculateDetailedRevenue(
        Parameters @params,
        int tuNgayAsInt,
        int denNgayAsInt,
        long tuNgayAsBigInt,
        long denNgayAsBigInt,
        int checksumFacId,
        List<dynamic> bilInvoiceDetails
    )
    {
        var result = new Dictionary<string, object>();

        // Tính toán doanh thu từ BIL_InvoiceDetail
        var bilDoanhThu = (
            from b in bilInvoiceDetails
            where b.IsRefund != true && !b.Reason.Contains("Lưu doanh thu vaccine")
            group b by new
            {
                b.PatientId,
                b.FacAdmissionId,
                b.Reason,
                b.RefundType,
                b.IsRefund,
                b.TongTienGiam,
            } into g
            select new
            {
                PatientPay = Math.Round(g.Sum(g1 => g1.PatientPay ?? 0), 0),
                TongTienGiam = g.Key.TongTienGiam > 0
                    ? g.Key.TongTienGiam ?? 0
                    : Math.Round(g.Sum(g1 => g1.SoTienGiam ?? 0), 0),
            }
        ).ToList();

        decimal doanhThu = bilDoanhThu.Sum(b => b.PatientPay) - bilDoanhThu.Sum(b => b.TongTienGiam);
        result["DoanhThu"] = doanhThu;

        // Tính toán hoàn phí
        decimal hoanPhi = (
            from a in db.QAHosGenericDB.BilInvoiceRefunds.With(SqlServerHints.Table.NoLock)
            from b in db
                .QAHosGenericDB.BilInvoiceRefundDetails.With(SqlServerHints.Table.NoLock)
                .Where(b => b.InvoiceRefundId == a.InvoiceRefundId)
            from bi in db
                .QAHosGenericDB.BilInvoices.With(SqlServerHints.Table.NoLock)
                .LeftJoin(bi => bi.InvoiceId == b.InvoiceId)
            where b.RefundType == 2
            group new { b, bi } by new { bi.InvoiceId, bi.RealTotal } into g
            select g.Key.RealTotal ?? 0
        ).Sum();
        result["HoanPhi"] = hoanPhi;

        // Tính toán thực thu
        decimal thucThu = CalcRealTotal(
            @params.FacId,
            tuNgayAsBigInt,
            denNgayAsBigInt,
            tuNgayAsInt,
            denNgayAsInt,
            checksumFacId
        );
        result["ThucThu"] = thucThu;

        // Tính toán doanh thu QA Pay
        decimal doanhThuQaPay = (
            from biq in db.QAHosGenericDB.BilInvoiceQapays.With(SqlServerHints.Table.NoLock)
            where biq.CheckSumFacId == checksumFacId && biq.CreatedOn.AsDate().Between(@params.TuNgay, @params.DenNgay)
            select biq.RealTotal ?? 0
        ).Sum();
        result["DoanhThuQaPay"] = doanhThuQaPay;

        // Tính toán doanh thu bán thẻ
        var bilInvoiceBusinesses = (
            from ib in db.QAHosGenericDB.BilInvoiceBusinesses.With(SqlServerHints.Table.NoLock)
            from s in db
                .QAHosGenericDB.LShiftDailies.With(SqlServerHints.Table.NoLock)
                .Where(s => s.ShiftDailyId == ib.ShiftDailyId)
            from ibd in db
                .QAHosGenericDB.BilInvoiceBusinessDetails.With(SqlServerHints.Table.NoLock)
                .Where(ibd => ibd.InvoiceBusinessId == ib.InvoiceBusinessId)
            where
                ib.IsRefund != true
                && s.NgayDoanhThu.AsDate().Between(@params.TuNgay, @params.DenNgay)
                && ib.FacId == @params.FacId
                && ibd.Serial != null
            select ibd.PatientPay ?? 0
        ).ToList();

        var bilInvoiceBusinessRefundTracks = (
            from ibrt in db.QAHosGenericDB.BilInvoiceBusinessRefundTracks.With(SqlServerHints.Table.NoLock)
            from s in db
                .QAHosGenericDB.LShiftDailies.With(SqlServerHints.Table.NoLock)
                .Where(s => s.ShiftDailyId == ibrt.ShiftDailyId)
            from ibd in db
                .QAHosGenericDB.BilInvoiceBusinessDetails.With(SqlServerHints.Table.NoLock)
                .Where(ibd => ibd.InvoiceBusinessId == ibrt.InvoiceId)
            from p in masterDataService.ListProducts(@params.FacId).Where(p => p.ProductId == ibd.ProductId)
            where
                (ibrt.RefundType ?? 0) == 0
                && ibrt.IsLastest == true
                && p.ProductTypeId == 23
                && s.NgayDoanhThu.AsDate().Between(@params.TuNgay, @params.DenNgay)
                && ibrt.FacId == @params.FacId
            select ibd.PatientPay ?? 0
        ).ToList();

        int soLuongThe = bilInvoiceBusinesses.Count + bilInvoiceBusinessRefundTracks.Count;
        decimal doanhThuBanThe = bilInvoiceBusinesses.Sum() + bilInvoiceBusinessRefundTracks.Sum();
        result["SoLuongThe"] = soLuongThe;
        result["DoanhThuBanThe"] = doanhThuBanThe;

        // Tính toán doanh thu online
        decimal doanhThuOnline = (
            from t in bilInvoiceDetails
            from biq in db
                .QAHosGenericDB.BilInvoiceAnotherSources.With(SqlServerHints.Table.NoLock)
                .Where(biq => biq.InvoiceIdGroup == t.InvoiceId)
            where t.IsRefund != true
            select t.RealTotal ?? 0
        ).Sum();
        result["DoanhThuOnline"] = doanhThuOnline;

        // Tính toán doanh thu đặt trước
        var bilDatTruocs = (
            from b in bilInvoiceDetails
            where
                b.ServiceId != 1
                && b.IsRefund != true
                && !b.Reason.Contains("Lưu doanh thu vaccine")
                && b.Loai == "Đặt trước"
            select new { b.PatientPay, b.SoTienGiam }
        ).ToList();
        decimal tongBilDatTruoc =
            bilDatTruocs.Sum(b => b.PatientPay ?? 0) - bilDatTruocs.Sum(b => b.SoTienGiam ?? 0);
        result["TongBilDatTruoc"] = tongBilDatTruoc;

        // Tính toán doanh thu hợp đồng
        var bilHopDongs = (
            from b in bilInvoiceDetails
            where
                b.ServiceId != 1
                && b.IsRefund != true
                && b.NoiDung.Contains("Thu tạm ứng")
                && b.Loai == "Hợp đồng"
                && b.NgayHopDongAsInt == tuNgayAsBigInt
            select new { b.PatientPay, b.SoTienGiam }
        ).ToList();
        decimal tongBilHopDong = bilHopDongs.Sum(b => b.PatientPay ?? 0) - bilHopDongs.Sum(b => b.SoTienGiam ?? 0);
        result["TongBilHopDong"] = tongBilHopDong;

        // Tính toán doanh thu khách lẻ
        var bilKhachLes = (
            from b in bilInvoiceDetails
            where
                b.ServiceId != 1
                && b.IsRefund != true
                && !b.Reason.Contains("Lưu doanh thu vaccine")
                && b.Loai is "" or "Khách lẻ"
            select new { b.PatientPay, b.SoTienGiam }
        ).ToList();
        decimal tongBilKhachLe = bilKhachLes.Sum(b => b.PatientPay ?? 0) - bilKhachLes.Sum(b => b.SoTienGiam ?? 0);
        result["TongBilKhachLe"] = tongBilKhachLe;

        return result;
    }

    // Tương ứng với file backup lines 600-800: CalculateOtherStatistics
    private Dictionary<string, object> CalculateOtherStatistics(
        Parameters @params,
        int tuNgayAsInt,
        int denNgayAsInt,
        List<FacAdmissionDto> facAdmissions,
        List<ClinicalSessionDto> clinicalSessions
    )
    {
        var result = new Dictionary<string, object>();

        // Tính toán tổng khách lỗi
        var bilInvoiceDetails = GetBilInvoiceDetails(@params, tuNgayAsInt * 1_000_000L, denNgayAsInt * 1_000_000L + 235959, DataUtils.Checksum(@params.FacId));
        var tongKhachLoi = bilInvoiceDetails
            .Where(t => t.Reason.Contains("Lỗi"))
            .Select(t => t.PatientId)
            .Distinct()
            .Count();
        result["TongKhachLoi"] = tongKhachLoi;

        // Tính toán số khách double
        var soKhachDouble = facAdmissions
            .GroupBy(a => new { a.PatientId, a.AdmitDateAsInt })
            .Where(g => g.Count() > 1)
            .Count();
        result["SoKhachDouble"] = soKhachDouble;

        // Tính toán tổng số khách buổi sáng
        var tongSoKhachBuoiSang = facAdmissions
            .Where(a => a.IsChieu == false)
            .Count();
        result["TongSoKhachBuoiSang"] = tongSoKhachBuoiSang;

        // Tính toán khách BSGT
        var khachBsgt = clinicalSessions
            .Where(cs => cs.ServiceId == 1)
            .Count();
        result["KhachBsgt"] = khachBsgt;

        // Tính toán khách đi cùng
        var khachDiCung = db
            .QAHosGenericDB.MdmAccompanyCustomers.With(SqlServerHints.Table.NoLock)
            .Count(ac => ac.FacId == @params.FacId && ac.CreatedDateAsInt.Between(tuNgayAsInt, denNgayAsInt));
        result["KhachDiCung"] = khachDiCung;

        return result;
    }

    // Tương ứng với file backup lines 800-1000: Helper Functions
    private List<dynamic> GetBilInvoiceDetails(Parameters @params, long tuNgayAsBigInt, long denNgayAsBigInt, int checksumFacId)
    {
        return db
            .QAHosGenericDB.BilInvoiceDetails.With(SqlServerHints.Table.NoLock)
            .Where(bd =>
                bd.FacId == @params.FacId &&
                bd.CreatedDateAsInt.Between(tuNgayAsBigInt, denNgayAsBigInt)
            )
            .ToList();
    }

    private List<Guid> GetKhachHopDongs(Parameters @params, int tuNgayAsInt, int denNgayAsInt)
    {
        return db
            .QAHosGenericDB.VaccineHopDongs.With(SqlServerHints.Table.NoLock)
            .Where(hd =>
                hd.FacId == @params.FacId &&
                hd.CreatedDateAsInt.Between(tuNgayAsInt, denNgayAsInt) &&
                hd.IsPaid == true
            )
            .Select(hd => hd.PatientId)
            .ToList();
    }

    // Tương ứng với file backup lines 1134-1415: CalcRealTotal
    private Decimal CalcRealTotal(
        string facId,
        long tuNgayAsBigInt,
        long denNgayAsBigInt,
        int tuNgayAsInt,
        int denNgayAsInt,
        int checksumFacId
    )
    {
        // Tính toán từ các bảng thanh toán
        var tienMat = db
            .QAHosGenericDB.BilInvoiceCashes.With(SqlServerHints.Table.NoLock)
            .Where(bic => bic.FacId == facId && bic.CreatedDateAsInt.Between(tuNgayAsBigInt, denNgayAsBigInt))
            .Sum(bic => bic.RealTotal ?? 0);

        var chuyenKhoan = db
            .QAHosGenericDB.BilInvoiceTransfers.With(SqlServerHints.Table.NoLock)
            .Where(bit => bit.FacId == facId && bit.CreatedDateAsInt.Between(tuNgayAsBigInt, denNgayAsBigInt))
            .Sum(bit => bit.RealTotal ?? 0);

        var theTinDung = db
            .QAHosGenericDB.BilInvoiceCredits.With(SqlServerHints.Table.NoLock)
            .Where(bic => bic.FacId == facId && bic.CreatedDateAsInt.Between(tuNgayAsBigInt, denNgayAsBigInt))
            .Sum(bic => bic.RealTotal ?? 0);

        var khac = db
            .QAHosGenericDB.BilInvoiceOthers.With(SqlServerHints.Table.NoLock)
            .Where(bio => bio.FacId == facId && bio.CreatedDateAsInt.Between(tuNgayAsBigInt, denNgayAsBigInt))
            .Sum(bio => bio.RealTotal ?? 0);

        var voucher = db
            .QAHosGenericDB.BilInvoiceVouchers.With(SqlServerHints.Table.NoLock)
            .Where(biv => biv.FacId == facId && biv.CreatedDateAsInt.Between(tuNgayAsBigInt, denNgayAsBigInt))
            .Sum(biv => biv.RealTotal ?? 0);

        return tienMat + chuyenKhoan + theTinDung + khac + voucher;
    }

    // Tương ứng với file backup lines 1200-1500: Table Creation Functions
    private DataTable CreateTongQuanTable(
        Dictionary<string, object> detailedStats,
        Dictionary<string, object> detailedRevenue,
        Dictionary<string, object> otherStats
    )
    {
        var table = new DataTable("TongQuan");
        table.Columns.Add("ChiTieu", typeof(string));
        table.Columns.Add("GiaTri", typeof(object));

        // Thêm các chỉ số từ detailedStats
        if (detailedStats.ContainsKey("TiepNhanTheoNguon"))
        {
            var tiepNhanTheoNguon = (Dictionary<int, int>)detailedStats["TiepNhanTheoNguon"];
            foreach (var kvp in tiepNhanTheoNguon)
            {
                table.Rows.Add($"Tiếp nhận nguồn {kvp.Key}", kvp.Value);
            }
        }

        // Thêm các chỉ số khác
        table.Rows.Add("Khách đặt trước", detailedStats.GetValueOrDefault("SoKhachDatTruoc", 0));
        table.Rows.Add("Khách hợp đồng", detailedStats.GetValueOrDefault("SoKhachHopDong", 0));
        table.Rows.Add("Khách mới", detailedStats.GetValueOrDefault("TongSoLuotTnMoi", 0));
        table.Rows.Add("Khách khám lẻ", detailedStats.GetValueOrDefault("TongSoKhachKham", 0));
        table.Rows.Add("Khách khám hợp đồng", detailedStats.GetValueOrDefault("TongSoKhachKhamHd", 0));
        table.Rows.Add("Khách được tiêm", detailedStats.GetValueOrDefault("TongSoKhachDuocTiem", 0));
        table.Rows.Add("Khách không được tiêm", detailedStats.GetValueOrDefault("TongKhachKhongDuocTiem", 0));
        table.Rows.Add("Khách bỏ về", detailedStats.GetValueOrDefault("SoLuotBoVe", 0));
        table.Rows.Add("Khách đã tiêm", detailedStats.GetValueOrDefault("TongSoKhachDaTiem", 0));
        table.Rows.Add("Khách người lớn", detailedStats.GetValueOrDefault("TongSoNguoiLon", 0));
        table.Rows.Add("Khách khám người thân", detailedStats.GetValueOrDefault("TongSoKhamNguoiThan", 0));

        // Thêm các chỉ số doanh thu
        table.Rows.Add("Doanh thu", detailedRevenue.GetValueOrDefault("DoanhThu", 0m));
        table.Rows.Add("Hoàn phí", detailedRevenue.GetValueOrDefault("HoanPhi", 0m));
        table.Rows.Add("Thực thu", detailedRevenue.GetValueOrDefault("ThucThu", 0m));
        table.Rows.Add("Doanh thu QA Pay", detailedRevenue.GetValueOrDefault("DoanhThuQaPay", 0m));
        table.Rows.Add("Doanh thu bán thẻ", detailedRevenue.GetValueOrDefault("DoanhThuBanThe", 0m));
        table.Rows.Add("Doanh thu online", detailedRevenue.GetValueOrDefault("DoanhThuOnline", 0m));
        table.Rows.Add("Doanh thu đặt trước", detailedRevenue.GetValueOrDefault("TongBilDatTruoc", 0m));
        table.Rows.Add("Doanh thu hợp đồng", detailedRevenue.GetValueOrDefault("TongBilHopDong", 0m));
        table.Rows.Add("Doanh thu khách lẻ", detailedRevenue.GetValueOrDefault("TongBilKhachLe", 0m));

        // Thêm các chỉ số khác
        table.Rows.Add("Tổng khách lỗi", otherStats.GetValueOrDefault("TongKhachLoi", 0));
        table.Rows.Add("Số khách double", otherStats.GetValueOrDefault("SoKhachDouble", 0));
        table.Rows.Add("Tổng số khách buổi sáng", otherStats.GetValueOrDefault("TongSoKhachBuoiSang", 0));
        table.Rows.Add("Khách BSGT", otherStats.GetValueOrDefault("KhachBsgt", 0));
        table.Rows.Add("Khách đi cùng", otherStats.GetValueOrDefault("KhachDiCung", 0));

        return table;
    }

    private DataTable CreateTiemChungTable(Dictionary<string, object> detailedStats)
    {
        var table = new DataTable("TiemChung");
        table.Columns.Add("ChiTieu", typeof(string));
        table.Columns.Add("GiaTri", typeof(object));

        table.Rows.Add("Tổng số khách được tiêm", detailedStats.GetValueOrDefault("TongSoKhachDuocTiem", 0));
        table.Rows.Add("Tổng số khách không được tiêm", detailedStats.GetValueOrDefault("TongKhachKhongDuocTiem", 0));
        table.Rows.Add("Tổng số khách đã tiêm", detailedStats.GetValueOrDefault("TongSoKhachDaTiem", 0));

        return table;
    }

    private DataTable CreateKhachTiemTable(Dictionary<string, object> detailedStats)
    {
        var table = new DataTable("KhachTiem");
        table.Columns.Add("ChiTieu", typeof(string));
        table.Columns.Add("GiaTri", typeof(object));

        table.Rows.Add("Khách được tiêm", detailedStats.GetValueOrDefault("TongSoKhachDuocTiem", 0));
        table.Rows.Add("Khách không được tiêm", detailedStats.GetValueOrDefault("TongKhachKhongDuocTiem", 0));
        table.Rows.Add("Khách đã tiêm", detailedStats.GetValueOrDefault("TongSoKhachDaTiem", 0));

        return table;
    }

    private DataTable CreateBenhNhanHomNayTable(Parameters @params)
    {
        var table = new DataTable("BenhNhanHomNay");
        table.Columns.Add("ChiTieu", typeof(string));
        table.Columns.Add("GiaTri", typeof(object));

        var today = DateTime.Today;
        var todayAsInt = today.DateAsInt();

        var soBenhNhanHomNay = db
            .QAHosGenericDB.CnFacAdmissions.With(SqlServerHints.Table.NoLock)
            .Count(a => a.FacId == @params.FacId && a.AdmitDateAsInt == todayAsInt);

        table.Rows.Add("Số bệnh nhân hôm nay", soBenhNhanHomNay);

        return table;
    }

    private DataTable CreateBaoCaoVanBanTable(
        Parameters @params,
        Dictionary<string, object> detailedStats,
        Dictionary<string, object> detailedRevenue,
        Dictionary<string, object> otherStats
    )
    {
        var table = new DataTable("BaoCaoVanBan");
        table.Columns.Add("ChiTieu", typeof(string));
        table.Columns.Add("GiaTri", typeof(object));

        // Tổng hợp tất cả các chỉ số
        var tongTiepNhan = detailedStats.G
