// using System;
// using System.ComponentModel;
// using System.Data;
// using System.Diagnostics.Metrics;
// using System.Globalization;
// using System.Linq;
// using System.Text;
// using Aladdin.Entities;
// using Aladdin.Entities.QAHosGenericDB;
// using Aladdin.Services;
// using Aladdin.Utilities;
// using AutoMapper;
// using AutoMapper.QueryableExtensions;
// using LinqToDB;
// using LinqToDB.DataProvider.SqlServer;

// namespace Aladdin.WebService.Handlers.QAHosGenericDB;

// // ReSharper disable once InconsistentNaming
// // ReSharper disable once UnusedType.Global
// public class ws_QuanLyTapTrung_BK(
//     AladdinDataConnection db,
//     DateTimeService dateTimeService,
//     MasterDataService masterDataService,
//     SettingsService settingsService
// ) : GenericHandler<ws_QuanLyTapTrung.Parameters>
// {
//     public class Parameters
//     {
//         public DateTime TuNgay { get; set; }
//         public DateTime DenNgay { get; set; }
//         public string FacId { get; set; }

//         [DisplayName("_Type")]
//         public int Type { get; set; } = 0;
//     }

//     private class FacAdmissionDto
//     {
//         public Guid FacAdmissionId { get; init; }
//         public int? NguonTiepNhan { get; init; }
//         public Guid? PatientId { get; init; }
//         public string? FacId { get; init; }
//         public Guid? CreatedBy { get; init; }
//         public DateTime? DischargedOn { get; init; }
//         public DateTime? AdmitDate { get; init; }
//         public int? AdmitDateAsInt { get; init; }
//         public DateTime? AdmitOn { get; init; }
//         public int? TuoiAsInt { get; init; }
//         public bool? IsChieu { get; init; }
//     }

//     // ReSharper disable ClassNeverInstantiated.Local
//     private class ClinicalSessionDto
//     {
//         public Guid ClinicalSessionId { get; set; }
//         public Guid? FacAdmissionId { get; set; }
//         public Guid? PhysicianAdmissionId { get; set; }
//         public Guid? PatientId { get; set; }
//         public int? ServiceId { get; set; }
//         public Guid? HopDongId { get; set; }
//         public DateTime? CompletedOn { get; set; }
//         public int? ProductTypeId { get; set; }
//         public bool? IsDuocTiem { get; set; }
//         public int? RoomId { get; set; }
//         public int? ServiceTypeId { get; set; }
//         public string? FacId { get; set; }
//     }

//     private class PhysicianAdmissionDto
//     {
//         public Guid PhysicianAdmissionId { get; set; }
//         public DateTime? DischargedOn { get; set; }
//         public bool? IsKhongDuocTiem { get; set; }
//         public Guid? PatientId { get; set; }
//         public Guid? PrimaryDoctor { get; set; }
//         public int? RoomId { get; set; }
//         public Guid? FacAdmissionId { get; set; }
//         public DateTime? AdmitDate { get; set; }
//         public string? FacId { get; set; }
//     }

//     private class InvApprovedOutDto
//     {
//         public string? ApprovedOutNo { get; set; }
//         public Guid ApprovedOutId { get; set; }
//         public string? FacId { get; set; }
//         public int? RequestStockId { get; set; }
//         public DateTime? CreatedOn { get; set; }
//     }

//     private class BilInvoiceRefundDto
//     {
//         public Guid InvoiceRefundId { get; set; }
//     }

//     private class HopDongDto
//     {
//         public Guid HopDongId { get; set; }
//         public decimal? GiaTriHd { get; set; }
//         public decimal? SoTienGiam { get; set; }
//         public Guid? PatientId { get; set; }
//     }

//     private static readonly MapperConfiguration s_mapperConfig = new MapperConfiguration(cfg =>
//     {
//         cfg.CreateProjection<VaccineHopDong, HopDongDto>();
//         cfg.CreateProjection<CnFacAdmission, FacAdmissionDto>();
//         cfg.CreateProjection<CnClinicalSession, ClinicalSessionDto>();
//         cfg.CreateProjection<CnPhysicianAdmission, PhysicianAdmissionDto>();
//         cfg.CreateProjection<InvApprovedOut, InvApprovedOutDto>();
//         cfg.CreateProjection<BilInvoiceRefund, BilInvoiceRefundDto>();
//     });

//     public override DataSet Handle(Parameters @params)
//     {
//         int tuNgayAsInt = @params.TuNgay.DateAsInt();
//         int denNgayAsInt = @params.DenNgay.DateAsInt();
//         long tuNgayAsBigInt = tuNgayAsInt * 1_000_000L;
//         long denNgayAsBigInt = denNgayAsInt * 1_000_000L + 235959;
//         var tuNgay = @params.TuNgay.Date;
//         var denNgay = @params.DenNgay.Date;
//         int checksumFacId = DataUtils.Checksum(@params.FacId);

//         var facAdmissionsQuery = db
//             .QAHosGenericDB.CnFacAdmissions.With(SqlServerHints.Table.NoLock)
//             .Where(a => a.FacId == @params.FacId && a.AdmitDateAsInt.Between(tuNgayAsInt, denNgayAsInt))
//             .ProjectTo<FacAdmissionDto>(s_mapperConfig);

//         var facAdmissionsWithTuoiQuery =
//             from a in facAdmissionsQuery
//             from p in db
//                 .QAHosGenericDB.MdmPatients.With(SqlServerHints.Table.NoLock)
//                 .LeftJoin(p => p.PatientId == a.PatientId)
//             select new FacAdmissionDto
//             {
//                 FacAdmissionId = a.FacAdmissionId,
//                 NguonTiepNhan = a.NguonTiepNhan,
//                 PatientId = a.PatientId,
//                 FacId = a.FacId,
//                 CreatedBy = a.CreatedBy,
//                 DischargedOn = a.DischargedOn,
//                 AdmitDate = a.AdmitDate,
//                 AdmitDateAsInt = a.AdmitDateAsInt,
//                 AdmitOn = a.AdmitOn,
//                 TuoiAsInt = SqlFn.DateDiff(SqlFn.DateParts.Year, p.DoB, a.AdmitOn),
//                 IsChieu = a.IsChieu,
//             };

//         var clinicalSessionsQuery = db
//             .QAHosGenericDB.CnClinicalSessions.With(SqlServerHints.Table.NoLock)
//             .Where(a =>
//                 a.UserCreatedDateAsInt.Between(tuNgayAsInt, denNgayAsInt)
//                 && facAdmissionsQuery.Any(fa => fa.PatientId == a.PatientId)
//             )
//             .ProjectTo<ClinicalSessionDto>(s_mapperConfig);

//         var clinicalSessionsVaccineQuery =
//             from t in clinicalSessionsQuery
//             from cs in db
//                 .QAHosGenericDB.CnClinicalSessionIdVaccines.With(SqlServerHints.Table.NoLock)
//                 .Where(cs => cs.ClinicalSessionId == t.ClinicalSessionId)
//             where
//                 (cs.FacIdChiDinhChecksum == checksumFacId && cs.NgayChiDinhAsInt.Between(tuNgayAsInt, denNgayAsInt))
//                 || (cs.FacIdDaTiemChecksum == checksumFacId && cs.NgayTiemAsInt.Between(tuNgayAsInt, denNgayAsInt))
//             select new
//             {
//                 cs.ClinicalSessionId,
//                 cs.NgayTiemAsInt,
//                 t.PatientId,
//                 t.CompletedOn,
//                 t.ProductTypeId,
//                 t.IsDuocTiem,
//                 t.PhysicianAdmissionId,
//                 cs.RoomIdTiem,
//                 cs.FacIdDaTiem,
//                 cs.RoomIdChiDinh,
//                 cs.FacIdChiDinh,
//             };

//         var tempBilInvoiceQuery =
//             from b in db
//                 .QAHosGenericDB.BilInvoices.With(SqlServerHints.Table.NoLock)
//                 .Where(b =>
//                     b.CheckSumFacId == checksumFacId && b.CreatedDateAsInt.Between(tuNgayAsBigInt, denNgayAsBigInt)
//                 )
//             from hd in db
//                 .QAHosGenericDB.VaccineHopDongs.With(SqlServerHints.Table.NoLock)
//                 .LeftJoin(hd => hd.HopDongId == b.HopDongId)
//             select new
//             {
//                 b.InvoiceId,
//                 b.IsRefund,
//                 b.Reason,
//                 b.TongTienGiam,
//                 b.PatientId,
//                 b.FacAdmissionId,
//                 b.RefundType,
//                 b.PhysicianAdmissionId,
//                 b.DoiTuongId,
//                 b.InvoiceNo,
//                 b.RealTotal,
//                 b.HopDongId,
//                 b.CounterId,
//                 b.ReceiptNumber,
//                 b.Description,
//                 b.HinhThucThanhToan,
//                 b.CreatedByUser,
//                 b.CreatedOnByUser,
//                 b.IsVat,
//                 b.LanThu,
//                 NgayHopDongAsInt = SqlFn.TryCast<long>(SqlFn.Format(hd.NgayHopDong, "yyyyMMdd000000")),
//             };

//         var bilInvoiceDetailsQuery =
//             from a in tempBilInvoiceQuery
//             from b in db
//                 .QAHosGenericDB.BilInvoiceDetails.With(SqlServerHints.Table.NoLock)
//                 .Where(b => b.InvoiceId == a.InvoiceId)
//             select new
//             {
//                 b.ClinicalSessionId,
//                 b.PatientPay,
//                 b.SoTienGiam,
//                 b.ServiceId,
//                 b.NoiDung,
//                 Loai = a.HopDongId != null ? "Hợp đồng"
//                 : b.IsReserved == true ? "Đặt trước"
//                 : "",
//                 a.PatientId,
//                 a.InvoiceId,
//                 a.FacAdmissionId,
//                 a.PhysicianAdmissionId,
//                 a.Reason,
//                 a.RefundType,
//                 a.IsRefund,
//                 a.TongTienGiam,
//                 a.CounterId,
//                 a.ReceiptNumber,
//                 a.Description,
//                 a.HinhThucThanhToan,
//                 a.CreatedByUser,
//                 a.CreatedOnByUser,
//                 a.IsVat,
//                 a.DoiTuongId,
//                 a.InvoiceNo,
//                 a.RealTotal,
//                 a.LanThu,
//                 b.IsReserved,
//                 a.NgayHopDongAsInt,
//             };

//         var physicianAdmissionsQuery = db
//             .QAHosGenericDB.CnPhysicianAdmissions.With(SqlServerHints.Table.NoLock)
//             .Where(a =>
//                 a.FacId == @params.FacId && a.AdmitDateAsInt.Between(tuNgayAsInt, denNgayAsInt) && a.RoomId != 0
//             )
//             .ProjectTo<PhysicianAdmissionDto>(s_mapperConfig);

//         var invApprovedOutsQuery = db
//             .QAHosGenericDB.InvApprovedOuts.With(SqlServerHints.Table.NoLock)
//             .Where(inv =>
//                 new List<int?> { 104, 105, 106, 107 }.Contains(inv.OutTypeId)
//                 && inv.FacId == @params.FacId
//                 && inv.KhoXuatNgayXuatAsInt.Between(tuNgayAsInt, denNgayAsInt)
//             )
//             .ProjectTo<InvApprovedOutDto>(s_mapperConfig);

//         var bilInvoiceRefundQuery = db
//             .QAHosGenericDB.BilInvoiceRefunds.With(SqlServerHints.Table.NoLock)
//             .Where(a => a.FacId == @params.FacId && a.RefundOnAsInt.Between(tuNgayAsInt, denNgayAsInt))
//             .ProjectTo<BilInvoiceRefundDto>(s_mapperConfig);

//         var dataSet = new DataSet();
//         if (@params.Type == 1)
//         {
//             var facAdmissions = facAdmissionsWithTuoiQuery.ToList();
//             var clinicalSessionsVaccine = clinicalSessionsVaccineQuery.ToList();
//             var physicianAdmissions = physicianAdmissionsQuery.ToList();
//             var bilInvoiceDetails = bilInvoiceDetailsQuery.ToList();
//             int tiepNhanTong = facAdmissions
//                 .GroupBy(a => a.AdmitDate)
//                 .Select(g => g.Select(x => x.PatientId).Distinct().Count())
//                 .Sum();
//             var tiepNhanTheoNguon = new Dictionary<int, int>();
//             for (int nguonTiepNhan = 1; nguonTiepNhan <= 7; nguonTiepNhan++)
//             {
//                 int soLuong = facAdmissions
//                     .Where(a => a.NguonTiepNhan == nguonTiepNhan)
//                     .GroupBy(a => a.AdmitDate)
//                     .Select(g => g.Select(x => x.PatientId).Distinct().Count())
//                     .Sum();
//                 tiepNhanTheoNguon[nguonTiepNhan] = soLuong;
//             }

//             var khachDatTruocs = bilInvoiceDetails
//                 .Where(t => t.Loai == "Đặt trước")
//                 .Select(t => t.PatientId)
//                 .ToHashSet();
//             int soKhachDatTruoc = khachDatTruocs.Count;
//             int soKhachDatTruocCoKham = facAdmissions
//                 .Where(a => khachDatTruocs.Contains(a.PatientId ?? Guid.Empty))
//                 .Select(a => a.PatientId)
//                 .Distinct()
//                 .Count();

//             var khachHopDongs = (
//                 from hd in db.QAHosGenericDB.VaccineHopDongs.With(SqlServerHints.Table.NoLock)
//                 where hd.FacId == @params.FacId && hd.NgayHopDong.AsDate().Between(tuNgay, denNgay) && hd.IsPaid == true
//                 select hd.PatientId
//             ).ToList();
//             int soKhachHopDong = khachHopDongs.Count;
//             int soKhachHopDongCoKham = facAdmissions
//                 .Where(a => khachHopDongs.Contains(a.PatientId))
//                 .DistinctBy(a => a.PatientId)
//                 .Count();

//             int tongSoLuotTnMoi = db
//                 .QAHosGenericDB.MdmPatients.With(SqlServerHints.Table.NoLock)
//                 .Count(p => p.FacId == @params.FacId && p.CreatedItemAsInt.Between(tuNgayAsInt, denNgayAsInt));

//             int tongSoKhachKham = (
//                 from cv in clinicalSessionsVaccineQuery
//                 from c in clinicalSessionsQuery.Where(c =>
//                     c.ClinicalSessionId == cv.ClinicalSessionId && c.HopDongId == null
//                 )
//                 select c.PatientId
//             )
//                 .Distinct()
//                 .Count();

//             int tongSoKhachKhamHd = (
//                 from cv in clinicalSessionsVaccineQuery
//                 from c in clinicalSessionsQuery.Where(c =>
//                     c.ClinicalSessionId == cv.ClinicalSessionId && c.HopDongId != null
//                 )
//                 select c.PatientId
//             )
//                 .Distinct()
//                 .Count();

//             int tongSoKhachDuocTiem = clinicalSessionsVaccine.Select(t => t.PatientId).Distinct().Count();

//             int tongKhachKhongDuocTiem = physicianAdmissions.Count(a =>
//                 a.IsKhongDuocTiem == true && a.DischargedOn != null
//             );

//             int soLuotBoVe = (
//                 from a in facAdmissionsQuery
//                 from b in db
//                     .QAHosGenericDB.CnDoctorDecisions.With(SqlServerHints.Table.NoLock)
//                     .Where(b => b.FacAdmissionId == a.FacAdmissionId && b.FinalDecisionId != 1)
//                 select 1
//             ).Count();

//             int tongSoKhachDaTiem = clinicalSessionsVaccine
//                 .Where(c => c.NgayTiemAsInt != null && c.NgayTiemAsInt != 29990101)
//                 .DistinctBy(c => c.PatientId)
//                 .Count();

//             int tongSoNguoiLon = facAdmissions
//                 .Where(a => a.TuoiAsInt >= 18)
//                 .Select(a => new { a.PatientId, a.AdmitDateAsInt })
//                 .Distinct()
//                 .Count();

//             int tongSoKhamNguoiThan = (
//                 from b in clinicalSessionsQuery
//                 from c in physicianAdmissionsQuery.Where(c => c.PhysicianAdmissionId == b.PhysicianAdmissionId)
//                 where
//                     b.ServiceTypeId == 1
//                     && db.QAHosGenericDB.LDepartmentRooms.With(SqlServerHints.Table.NoLock)
//                         .Any(d => d.RoomId == b.RoomId && d.RoomName.Contains("Người thân") && d.FacId == @params.FacId)
//                 select b.PatientId
//             )
//                 .Distinct()
//                 .Count();

//             int tongSoMuiTiem = (
//                 from a in invApprovedOutsQuery
//                 from b in db
//                     .QAHosGenericDB.InvApprovedOutDetails.With(SqlServerHints.Table.NoLock)
//                     .Where(b => b.ApprovedOutId == a.ApprovedOutId)
//                 from c in db
//                     .QAHosGenericDB.LProducts.With(SqlServerHints.Table.NoLock)
//                     .Where(c => c.ProductId == b.ProductId && c.FacId == a.FacId)
//                 where c.ProductTypeId == 17
//                 select 1
//             ).Count();
//             decimal heSoMuiTiem = tongSoKhachDaTiem != 0 ? (decimal)tongSoMuiTiem / tongSoKhachDaTiem : 0;

//             var bilDoanhThu = (
//                 from b in bilInvoiceDetails
//                 where b.IsRefund != true && !b.Reason.Contains("Lưu doanh thu vaccine")
//                 group b by new
//                 {
//                     b.PatientId,
//                     b.FacAdmissionId,
//                     b.Reason,
//                     b.RefundType,
//                     b.IsRefund,
//                     b.TongTienGiam,
//                 } into g
//                 select new
//                 {
//                     PatientPay = Math.Round(g.Sum(g1 => g1.PatientPay ?? 0), 0),
//                     TongTienGiam = g.Key.TongTienGiam > 0
//                         ? g.Key.TongTienGiam ?? 0
//                         : Math.Round(g.Sum(g1 => g1.SoTienGiam ?? 0), 0),
//                 }
//             ).ToList();

//             decimal doanhThu = bilDoanhThu.Sum(b => b.PatientPay) - bilDoanhThu.Sum(b => b.TongTienGiam);

//             decimal hoanPhi = (
//                 from a in bilInvoiceRefundQuery
//                 from b in db
//                     .QAHosGenericDB.BilInvoiceRefundDetails.With(SqlServerHints.Table.NoLock)
//                     .Where(b => b.InvoiceRefundId == a.InvoiceRefundId)
//                 from bi in db
//                     .QAHosGenericDB.BilInvoices.With(SqlServerHints.Table.NoLock)
//                     .LeftJoin(bi => bi.InvoiceId == b.InvoiceId)
//                 where b.RefundType == 2
//                 group new { b, bi } by new { bi.InvoiceId, bi.RealTotal } into g
//                 select g.Key.RealTotal ?? 0
//             ).Sum();

//             //Calc thuc thu
//             decimal thucThu = CalcRealTotal(
//                 @params.FacId,
//                 tuNgayAsBigInt,
//                 denNgayAsBigInt,
//                 tuNgayAsInt,
//                 denNgayAsInt,
//                 checksumFacId
//             );

//             decimal doanhThuQaPay = (
//                 from biq in db.QAHosGenericDB.BilInvoiceQapays.With(SqlServerHints.Table.NoLock)
//                 where biq.CheckSumFacId == checksumFacId && biq.CreatedOn.AsDate().Between(tuNgay, denNgay)
//                 select biq.RealTotal ?? 0
//             ).Sum();

//             var bilInvoiceBusinesses = (
//                 from ib in db.QAHosGenericDB.BilInvoiceBusinesses.With(SqlServerHints.Table.NoLock)
//                 from s in db
//                     .QAHosGenericDB.LShiftDailies.With(SqlServerHints.Table.NoLock)
//                     .Where(s => s.ShiftDailyId == ib.ShiftDailyId)
//                 from ibd in db
//                     .QAHosGenericDB.BilInvoiceBusinessDetails.With(SqlServerHints.Table.NoLock)
//                     .Where(ibd => ibd.InvoiceBusinessId == ib.InvoiceBusinessId)
//                 where
//                     ib.IsRefund != true
//                     && s.NgayDoanhThu.AsDate().Between(tuNgay, denNgay)
//                     && ib.FacId == @params.FacId
//                     && ibd.Serial != null
//                 select ibd.PatientPay ?? 0
//             ).ToList();

//             var bilInvoiceBusinessRefundTracks = (
//                 from ibrt in db.QAHosGenericDB.BilInvoiceBusinessRefundTracks.With(SqlServerHints.Table.NoLock)
//                 from s in db
//                     .QAHosGenericDB.LShiftDailies.With(SqlServerHints.Table.NoLock)
//                     .Where(s => s.ShiftDailyId == ibrt.ShiftDailyId)
//                 from ibd in db
//                     .QAHosGenericDB.BilInvoiceBusinessDetails.With(SqlServerHints.Table.NoLock)
//                     .Where(ibd => ibd.InvoiceBusinessId == ibrt.InvoiceId)
//                 from p in masterDataService.ListProducts(@params.FacId).Where(p => p.ProductId == ibd.ProductId)
//                 where
//                     (ibrt.RefundType ?? 0) == 0
//                     && ibrt.IsLastest == true
//                     && p.ProductTypeId == 23
//                     && s.NgayDoanhThu.AsDate().Between(tuNgay, denNgay)
//                     && ibrt.FacId == @params.FacId
//                 select ibd.PatientPay ?? 0
//             ).ToList();
//             int soLuongThe = bilInvoiceBusinesses.Count + bilInvoiceBusinessRefundTracks.Count;
//             decimal doanhThuBanThe = bilInvoiceBusinesses.Sum() + bilInvoiceBusinessRefundTracks.Sum();

//             decimal doanhThuOnline = (
//                 from t in tempBilInvoiceQuery
//                 from biq in db
//                     .QAHosGenericDB.BilInvoiceAnotherSources.With(SqlServerHints.Table.NoLock)
//                     .Where(biq => biq.InvoiceIdGroup == t.InvoiceId)
//                 where t.IsRefund != true
//                 select t.RealTotal ?? 0
//             ).Sum();

//             var bilDatTruocs = (
//                 from b in bilInvoiceDetails
//                 where
//                     b.ServiceId != 1
//                     && b.IsRefund != true
//                     && !b.Reason.Contains("Lưu doanh thu vaccine")
//                     && b.Loai == "Đặt trước"
//                 select new { b.PatientPay, b.SoTienGiam }
//             ).ToList();
//             decimal tongBilDatTruoc =
//                 bilDatTruocs.Sum(b => b.PatientPay ?? 0) - bilDatTruocs.Sum(b => b.SoTienGiam ?? 0);

//             var bilHopDongs = (
//                 from b in bilInvoiceDetails
//                 where
//                     b.ServiceId != 1
//                     && b.IsRefund != true
//                     && b.NoiDung.Contains("Thu tạm ứng")
//                     && b.Loai == "Hợp đồng"
//                     && b.NgayHopDongAsInt == tuNgayAsBigInt
//                 select new { b.PatientPay, b.SoTienGiam }
//             ).ToList();
//             decimal tongBilHopDong = bilHopDongs.Sum(b => b.PatientPay ?? 0) - bilHopDongs.Sum(b => b.SoTienGiam ?? 0);

//             var bilHopDongCus = (
//                 from b in bilInvoiceDetails
//                 where
//                     b.ServiceId != 1
//                     && b.IsRefund != true
//                     && b.NoiDung.Contains("Thu tạm ứng")
//                     && b.Loai == "Hợp đồng"
//                     && b.NgayHopDongAsInt != tuNgayAsBigInt
//                 select new { b.PatientPay, b.SoTienGiam }
//             ).ToList();
//             decimal tongBilHopDongCu =
//                 bilHopDongCus.Sum(b => b.PatientPay ?? 0) - bilHopDongCus.Sum(b => b.SoTienGiam ?? 0);
//             decimal tongThuGoi = tongBilHopDong + tongBilHopDongCu;

//             var bilKhachLes = (
//                 from b in bilInvoiceDetails
//                 where
//                     b.ServiceId != 1
//                     && b.IsRefund != true
//                     && !b.Reason.Contains("Lưu doanh thu vaccine")
//                     && b.Loai is "" or "Khách lẻ"
//                 select new { b.PatientPay, b.SoTienGiam }
//             ).ToList();
//             decimal tongBilKhachLe = bilKhachLes.Sum(b => b.PatientPay ?? 0) - bilKhachLes.Sum(b => b.SoTienGiam ?? 0);

//             var hopDongsQuery = db
//                 .QAHosGenericDB.VaccineHopDongs.With(SqlServerHints.Table.NoLock)
//                 .Where(hd =>
//                     hd.CreatedDateAsInt.Between(tuNgayAsInt, denNgayAsInt)
//                     && hd.FacId == @params.FacId
//                     && hd.IsPaid == true
//                 )
//                 .ProjectTo<HopDongDto>(s_mapperConfig);

//             var hopDongDetailsQuery =
//                 from t in hopDongsQuery
//                 from h in db
//                     .QAHosGenericDB.VaccineHopDongDetails.With(SqlServerHints.Table.NoLock)
//                     .Where(h => h.HopDongId == t.HopDongId)
//                 where
//                     (
//                         h.IsHuyMui == null
//                         && h.MuiThanhToan == true
//                         && h.IsMuiNgoaiDanhMuc == false
//                         && h.IsTiemNgoai != true
//                     )
//                     || h.IsHuyMui != null
//                 select new
//                 {
//                     ThanhTien = (h.GiaChenhLechChuaGiam ?? 0) > 0
//                     || ((h.GiaChenhLechChuaGiam ?? 0) == 0 && (h.GiaChenhLechTiemNgoai ?? 0) == 0)
//                         ? (h.GiaMuiTiem ?? 0) + (h.GiaChenhLechChuaGiam ?? 0)
//                         : (h.GiaMuiTiem ?? 0) + (h.GiaChenhLechTiemNgoai ?? 0),
//                     t.HopDongId,
//                     h.HopDongDetailId,
//                     h.IsHuyMui,
//                 };

//             var tienClByHopDongId = (
//                 from t in hopDongDetailsQuery
//                 from vhdd in db
//                     .QAHosGenericDB.VaccineHopDongDetailRoots.With(SqlServerHints.Table.NoLock)
//                     .Where(vhdd => vhdd.HopDongDetailId == t.HopDongDetailId)
//                 where t.IsHuyMui == true
//                 group new { t, vhdd } by t.HopDongId into g
//                 select new
//                 {
//                     HopDongId = g.Key,
//                     TienCL = g.Sum(g1 => g1.vhdd.GiaMuiTiem ?? 0)
//                         + g.Sum(g1 => g1.vhdd.GiaChenhLechChuaGiam ?? 0)
//                         - g.Sum(g1 => g1.vhdd.GiaTiemNgoai ?? 0),
//                 }
//             )
//                 .ToList()
//                 .ToDictionary(h => h.HopDongId, h => h.TienCL);

//             var tongThanhTienByHopDongId = (
//                 from h in hopDongDetailsQuery
//                 where h.IsHuyMui == null
//                 group h by h.HopDongId into g
//                 select new { HopDongId = g.Key, TongThanhTien = g.Sum(g1 => g1.ThanhTien) }
//             )
//                 .ToList()
//                 .ToDictionary(h => h.HopDongId, h => h.TongThanhTien);

//             var soTienGiamByHopDongId = (
//                 from hd in hopDongsQuery
//                 from h in db
//                     .QAHosGenericDB.VaccineHopDongDetailRoots.With(SqlServerHints.Table.NoLock)
//                     .Where(h => h.HopDongId == hd.HopDongId && h.IsMuiNgoaiDanhMuc == false && h.IsTiemNgoai == false)
//                 where h.HopDongId != null
//                 group h by h.HopDongId into g
//                 select new { HopDongId = g.Key ?? Guid.Empty, SoTienGiam = g.Sum(g1 => g1.TienGiam ?? 0) }
//             )
//                 .ToList()
//                 .ToDictionary(g => g.HopDongId, g => g.SoTienGiam);

//             var hopDongs1 = (
//                 from t in hopDongsQuery
//                 from hd in db
//                     .QAHosGenericDB.VaccineHopDongDetails.With(SqlServerHints.Table.NoLock)
//                     .Where(hd => hd.HopDongId == t.HopDongId)
//                 from d in db
//                     .QAHosGenericDB.VaccinePhacDoBenhNhanDetails.With(SqlServerHints.Table.NoLock)
//                     .Where(d =>
//                         d.PatientId == t.PatientId && d.IdPhacDoDetail == hd.MaMuiTiem && d.HopDongId == hd.HopDongId
//                     )
//                 select t
//             )
//                 .Distinct()
//                 .ToList();

//             foreach (var hd in hopDongs1)
//             {
//                 decimal tongThanhTien = tongThanhTienByHopDongId.GetValueOrDefault(hd.HopDongId);
//                 decimal tienCl = tienClByHopDongId.GetValueOrDefault(hd.HopDongId);
//                 hd.GiaTriHd = tongThanhTien - tienCl;
//                 hd.SoTienGiam = soTienGiamByHopDongId.GetValueOrDefault(hd.HopDongId);
//             }

//             decimal tongGiaTriGoiBanTrongNgay =
//                 hopDongs1.Sum(h => h.GiaTriHd ?? 0) - hopDongs1.Sum(h => h.SoTienGiam ?? 0);

//             // Các đợt khám không thêm mũi trong ngày
//             int tongKhachLoi = (
//                 from b in facAdmissionsQuery
//                 from a in clinicalSessionsQuery.LeftJoin(a => a.FacAdmissionId == b.FacAdmissionId)
//                 where a.FacAdmissionId == null && a.FacId == @params.FacId
//                 select new { b.PatientId, b.FacAdmissionId }
//             )
//                 .Distinct()
//                 .Count();

//             int soKhachDouble = (
//                 from a in facAdmissionsQuery
//                 from c in clinicalSessionsQuery.Where(c => c.FacAdmissionId == a.FacAdmissionId)
//                 where c.ServiceId == 1
//                 group new { a, c } by new { c.PatientId, a.AdmitDateAsInt } into g
//                 where g.Count() > 1
//                 select 1
//             ).Count();

//             int tongSoKhachBuoiSang = facAdmissions.Where(a => a.IsChieu == false).DistinctBy(a => a.PatientId).Count();

//             var khachDiCungs = (
//                 from a in db.QAHosGenericDB.MdmAccompanyCustomers.With(SqlServerHints.Table.NoLock)
//                 where a.CreatedDateAsInt.Between(tuNgayAsInt, denNgayAsInt) && a.FacIdCheckSum == checksumFacId
//                 select new { a.PatientId, a.ReservationType }
//             ).ToList();
//             int tongKhachBsgt = khachDiCungs.Where(a => a.ReservationType == "PK").DistinctBy(a => a.PatientId).Count();
//             int tongKhachDiCung = khachDiCungs.DistinctBy(a => a.PatientId).Count();

//             var bilKhachDiCungs = (
//                 from t in bilInvoiceDetailsQuery
//                 from ac in db
//                     .QAHosGenericDB.MdmAccompanyCustomers.With(SqlServerHints.Table.NoLock)
//                     .Where(ac => ac.PatientId == t.PatientId && ac.FacIdCheckSum == checksumFacId)
//                 where
//                     t.IsRefund == false
//                     && !t.Reason.Contains("Lưu doanh thu vaccine")
//                     && ac.CreatedDateAsInt.Between(tuNgayAsInt, denNgayAsInt)
//                 group t by new
//                 {
//                     t.PatientId,
//                     t.FacAdmissionId,
//                     t.Reason,
//                     t.RefundType,
//                     t.IsRefund,
//                     t.TongTienGiam,
//                     ac.ReservationType,
//                 } into g
//                 select new
//                 {
//                     g.Key.ReservationType,
//                     PatientPay = Math.Round(g.Sum(g1 => g1.PatientPay ?? 0), 0),
//                     TongTienGiam = g.Key.TongTienGiam > 0
//                         ? g.Key.TongTienGiam ?? 0
//                         : Math.Round(g.Sum(g1 => g1.SoTienGiam ?? 0), 0),
//                 }
//             ).ToList();

//             decimal doanhThuBsgt =
//                 bilKhachDiCungs.Where(b => b.ReservationType == "PK").Sum(b => b.PatientPay)
//                 - bilKhachDiCungs.Where(b => b.ReservationType == "PK").Sum(b => b.TongTienGiam);

//             decimal doanhThuKhDiCung =
//                 bilKhachDiCungs.Sum(b => b.PatientPay) - bilKhachDiCungs.Sum(b => b.TongTienGiam);

//             int khSuDungDvVip = (
//                 from c in db.QAHosGenericDB.CnClinicalSessions.With(SqlServerHints.Table.NoLock)
//                 where
//                     c.FacId == @params.FacId
//                     && c.UserCreatedDateAsInt.Between(tuNgayAsInt, denNgayAsInt)
//                     && c.ServiceId == 11024
//                     && c.IsPaid == true
//                 select c.PatientId
//             )
//                 .Distinct()
//                 .Count();

//             int facilityId = System.Convert.ToInt32(@params.FacId.Replace(".", ""));

//             var vipServiceIds = (
//                 from s in db.QAHosGenericDB.LServiceVipExaminations.With(SqlServerHints.Table.NoLock)
//                 where s.FacilityId == facilityId && s.ServiceId != 1
//                 select s.ServiceId
//             ).ToHashSet();

//             var bilKhSuDungDvVips = (
//                 from b in bilInvoiceDetails
//                 where
//                     b.IsRefund != true
//                     && b.Reason.Contains("Viện phí")
//                     && b.ServiceId != null
//                     && vipServiceIds.Contains(b.ServiceId ?? 0)
//                 group b by new
//                 {
//                     b.PatientId,
//                     b.FacAdmissionId,
//                     b.Reason,
//                     b.RefundType,
//                     b.IsRefund,
//                     b.TongTienGiam,
//                 } into g
//                 select new
//                 {
//                     PatientPay = Math.Round(g.Sum(g1 => g1.PatientPay ?? 0), 0),
//                     TongTienGiam = g.Key.TongTienGiam > 0
//                         ? g.Key.TongTienGiam ?? 0
//                         : Math.Round(g.Sum(g1 => g1.SoTienGiam ?? 0), 0),
//                 }
//             ).ToList();
//             decimal doanhThuKhSuDungDichVuVip =
//                 bilKhSuDungDvVips.Sum(b => b.PatientPay) - bilKhSuDungDvVips.Sum(b => b.TongTienGiam);

//             //Calculate for Store
//             var result = db
//                 .QAHosGenericDB.BilInvoiceBusinesses.Where(b =>
//                     b.InvoiceDateAsInt!.Value >= tuNgayAsInt
//                     && b.InvoiceDateAsInt.Value <= denNgayAsInt
//                     && b.Total!.Value > 0
//                     && b.FacId == @params.FacId
//                 )
//                 .GroupBy(b => b.FacId)
//                 .Select(g => new { SoGD = g.Count(), TongDoanhThu = g.Sum(x => x.Total ?? 0) })
//                 .FirstOrDefault();

//             int soGD = result?.SoGD ?? 0;
//             decimal tongDoanhThu = result?.TongDoanhThu ?? 0;

//             var cultureInfo = new CultureInfo("vi-VN");
//             var tempTongQuan = new List<object>
//             {
//                 new { DienGiai = "Tổng lượt tiếp nhận", GiaTri = tiepNhanTong.ToString() },
//                 new { DienGiai = "Tiếp nhận trực tiếp", GiaTri = tiepNhanTheoNguon[1].ToString() },
//                 new { DienGiai = "Nguồn tiếp nhận tổng đài", GiaTri = tiepNhanTheoNguon[2].ToString() },
//                 new { DienGiai = "Nguồn tiếp nhận người thân giới thiệu", GiaTri = tiepNhanTheoNguon[3].ToString() },
//                 new { DienGiai = "Nguồn tiếp nhận facebook", GiaTri = tiepNhanTheoNguon[4].ToString() },
//                 new { DienGiai = "Nguồn tiếp nhận truyền hình", GiaTri = tiepNhanTheoNguon[5].ToString() },
//                 new { DienGiai = "Nguồn tiếp nhận đi ngang qua thấy", GiaTri = tiepNhanTheoNguon[6].ToString() },
//                 new { DienGiai = "Nguồn tiếp nhận khác", GiaTri = tiepNhanTheoNguon[7].ToString() },
//                 new { DienGiai = "Tổng số khách đặt trước", GiaTri = soKhachDatTruoc.ToString() },
//                 new { DienGiai = "Tổng số hợp đồng", GiaTri = soKhachHopDong.ToString() },
//                 new { DienGiai = "Tổng số lượt tiếp nhận mới", GiaTri = tongSoLuotTnMoi.ToString() },
//                 new { DienGiai = "Tổng số khách khám lẻ", GiaTri = tongSoKhachKham.ToString() },
//                 new { DienGiai = "Tổng số khách khám hợp đồng", GiaTri = tongSoKhachKhamHd.ToString() },
//                 new { DienGiai = "Tổng số lượt khách được tiêm", GiaTri = tongSoKhachDuocTiem.ToString() },
//                 new { DienGiai = "Tổng số lượt khách không được tiêm", GiaTri = tongKhachKhongDuocTiem.ToString() },
//                 new { DienGiai = "Tổng số lượt khách bỏ về", GiaTri = soLuotBoVe.ToString() },
//                 new { DienGiai = "Tổng số khách đã tiêm", GiaTri = tongSoKhachDaTiem.ToString() },
//                 new { DienGiai = "Tổng số khách người lớn", GiaTri = tongSoNguoiLon.ToString() },
//                 new { DienGiai = "Tổng số khách hàng phòng khám người thân", GiaTri = tongSoKhamNguoiThan.ToString() },
//                 new { DienGiai = "Tổng số mũi tiêm", GiaTri = tongSoMuiTiem.ToString() },
//                 new { DienGiai = "Hệ số mũi tiêm", GiaTri = heSoMuiTiem.ToString("0.00") },
//                 new { DienGiai = "Doanh thu", GiaTri = doanhThu.ToString("C", cultureInfo) },
//                 new { DienGiai = "Hoàn phí", GiaTri = hoanPhi.ToString("C", cultureInfo) },
//                 new { DienGiai = "Thực thu", GiaTri = thucThu.ToString("C", cultureInfo) },
//                 new { DienGiai = "Doanh thu QAPay", GiaTri = doanhThuQaPay.ToString("C", cultureInfo) },
//                 new { DienGiai = "Doanh thu bán thẻ", GiaTri = doanhThuBanThe.ToString("C", cultureInfo) },
//                 new { DienGiai = "Doanh thu thanh toán online", GiaTri = doanhThuOnline.ToString("C", cultureInfo) },
//                 new { DienGiai = "Đặt trước", GiaTri = tongBilDatTruoc.ToString("C", cultureInfo) },
//                 new { DienGiai = "Thu gói", GiaTri = tongThuGoi.ToString("C", cultureInfo) },
//                 new
//                 {
//                     DienGiai = "Tổng giá trị gói bán trong ngày",
//                     GiaTri = tongGiaTriGoiBanTrongNgay.ToString("C", cultureInfo),
//                 },
//                 new { DienGiai = "Hợp đồng hôm nay", GiaTri = tongBilHopDong.ToString("C", cultureInfo) },
//                 new { DienGiai = "Hợp đồng cũ", GiaTri = tongBilHopDongCu.ToString("C", cultureInfo) },
//                 new { DienGiai = "Khách lẻ", GiaTri = tongBilKhachLe.ToString("C", cultureInfo) },
//                 new { DienGiai = "Số khách bị sai", GiaTri = tongKhachLoi.ToString() },
//                 new { DienGiai = "Tổng số khách có 2 công khám trở lên", GiaTri = soKhachDouble.ToString() },
//                 new { DienGiai = "Tổng số khách khám vào buổi sáng", GiaTri = tongSoKhachBuoiSang.ToString() },
//                 new { DienGiai = "Số lượng KH BSGT", GiaTri = tongKhachBsgt.ToString() },
//                 new { DienGiai = "Số lượng KH đi cùng", GiaTri = tongKhachDiCung.ToString() },
//                 new { DienGiai = "Doanh thu KH BSGT", GiaTri = doanhThuBsgt.ToString("C", cultureInfo) },
//                 new { DienGiai = "Doanh thu KH đi cùng", GiaTri = doanhThuKhDiCung.ToString("C", cultureInfo) },
//                 new { DienGiai = "KH sử dụng DV VIP", GiaTri = khSuDungDvVip.ToString() },
//                 new
//                 {
//                     DienGiai = "Doanh thu KH sử dụng DV VIP",
//                     GiaTri = doanhThuKhSuDungDichVuVip.ToString("C", cultureInfo),
//                 },
//                 new { DienGiai = "Số giao dịch VNVC Shop", GiaTri = soGD.ToString("C", cultureInfo) },
//                 new { DienGiai = "Tổng doanh thu VNVC Shop", GiaTri = tongDoanhThu.ToString("C", cultureInfo) },
//             };

//             //Table0
//             dataSet.Tables.Add(tempTongQuan.ToDataTable());

//             //Table1
//             dataSet.Tables.Add(
//                 new List<object>
//                 {
//                     new { Key = "Tổng số khách đã tiêm", Value = tongSoKhachDaTiem },
//                     new { Key = "Tổng số mũi tiêm", Value = tongSoMuiTiem },
//                 }.ToDataTable()
//             );

//             //Table2
//             dataSet.Tables.Add(
//                 new List<object>
//                 {
//                     new { Key = "Tổng số khách được tiêm", Value = tongSoKhachDuocTiem },
//                     new { Key = "Tổng số khách không được tiêm", Value = tongKhachKhongDuocTiem },
//                 }.ToDataTable()
//             );

//             //Table3
//             int tongBnHomNay = (
//                 from a in db.QAHosGenericDB.CnFacAdmissions.With(SqlServerHints.Table.NoLock)
//                 where a.AdmitDateAsInt == dateTimeService.Now().DateAsInt() && a.FacId == @params.FacId
//                 select a.PatientId
//             )
//                 .Distinct()
//                 .Count(); // Chỉ lấy ngày hôm nay, ko lấy theo ngày truyền vào

//             dataSet.Tables.Add(new List<object> { new { TongBN = tongBnHomNay } }.ToDataTable());

//             // Vaccine-HC/KK
//             var vaccineHanCheKhuyenKhichs = @params.FacId is "777" or "9"
//                 ? db
//                     .QAHosGenericDB.VaccineHanCheKhuyenKhiches.With(SqlServerHints.Table.NoLock)
//                     .Where(v => v.FacId == @params.FacId)
//                     .Select(v => new
//                     {
//                         v.VaccineId,
//                         v.VaccineName,
//                         v.TypeCode,
//                         v.ToDate,
//                     })
//                     .ToList()
//                 : db
//                     .QAHosGenericDB.VaccineHanCheKhuyenKhiches.With(SqlServerHints.Table.NoLock)
//                     .Where(v => v.FacId != "777" && v.FacId != "9")
//                     .Select(v => new
//                     {
//                         v.VaccineId,
//                         v.VaccineName,
//                         v.TypeCode,
//                         v.ToDate,
//                     })
//                     .ToList();

//             var approvedOutsByProductId = (
//                 from a in invApprovedOutsQuery
//                 from b in db
//                     .QAHosGenericDB.InvApprovedOutDetails.With(SqlServerHints.Table.NoLock)
//                     .Where(b => b.ApprovedOutId == a.ApprovedOutId)
//                 group b by b.ProductId into g
//                 select new { ProductId = g.Key, SL = g.Count() }
//             ).ToList();

//             string vaccineHanChes = (
//                 from v in vaccineHanCheKhuyenKhichs.Where(v => v.TypeCode == 0 && v.ToDate >= tuNgay)
//                 from a in approvedOutsByProductId.Where(a => a.ProductId == v.VaccineId).DefaultIfEmpty()
//                 select $"   - {v.VaccineName} : {a?.SL ?? 0}"
//             ).StringJoin("\n\n");

//             string vaccineKhuyenKhichs = (
//                 from v in vaccineHanCheKhuyenKhichs.Where(v => v.TypeCode == 1 && v.ToDate >= tuNgay)
//                 from a in approvedOutsByProductId.Where(a => a.ProductId == v.VaccineId).DefaultIfEmpty()
//                 select $"   - {v.VaccineName} : {a?.SL ?? 0}"
//             ).StringJoin("\n\n");

//             var customer = db
//                 .QAHosGenericDB.LCustomers.With(SqlServerHints.Table.NoLock)
//                 .Where(c => c.FacId == @params.FacId)
//                 .Select(c => new
//                 {
//                     FacName = c.CustomerFullName,
//                     c.NguoiDaiDien,
//                     TinhTp = c.ProvinceId,
//                 })
//                 .FirstOrDefault();

//             int tongKhach = facAdmissions.Count;
//             var sb = new StringBuilder();
//             // Initial blank line as per Table5 string
//             sb.Append("\n");

//             // Kính gửi: Tổng Giám Đốc \r  -> results in content + "\n\n"
//             sb.Append("Kính gửi: Tổng Giám Đốc ").Append("\n\n");

//             // {customer.FacName}\r      -> results in content + "\n \n" (note the space)
//             sb.Append(customer.FacName).Append("\n \n");

//             // Báo cáo ngày: ... \r       -> results in content + "\n\n"
//             sb.Append(
//                     "Báo cáo ngày: "
//                         + (
//                             tuNgayAsInt == denNgayAsInt
//                                 ? tuNgay.ToString("dd/MM/yyyy", cultureInfo)
//                                 : tuNgay.ToString("dd/MM/yyyy", cultureInfo)
//                                     + " - "
//                                     + denNgay.ToString("dd/MM/yyyy", cultureInfo)
//                         )
//                 )
//                 .Append("\n\n");

//             sb.Append($"1. Số tiếp nhận: {tiepNhanTong} KH").Append("\n\n");
//             sb.Append($"  KH người lớn:  {tongSoNguoiLon} KH").Append("\n\n");
//             sb.Append(
//                     "  % tỉ lệ KH người lớn:  "
//                         + (
//                             tiepNhanTheoNguon[1] > 0
//                                 ? ((float)tongSoNguoiLon / tiepNhanTheoNguon[1]).ToString("P2", cultureInfo)
//                                 : ""
//                         )
//                 )
//                 .Append("\n\n");
//             sb.Append($"  Số HĐ Gói: {soKhachHopDong}").Append("\n\n");
//             sb.Append(
//                     "  % tỉ lệ gói: "
//                         + (
//                             tiepNhanTheoNguon[1] > 0
//                                 ? ((float)soKhachHopDong / tiepNhanTheoNguon[1]).ToString("P2", cultureInfo)
//                                 : ""
//                         )
//                 )
//                 .Append("\n\n");
//             sb.Append("  Hệ số mũi tiêm:  " + heSoMuiTiem.ToString("0.00", cultureInfo)).Append("\n\n");
//             // Số lượng bán thẻ: {soLuongThe}\r  -> content + "\n \n"
//             sb.Append($"  Số lượng bán thẻ: {soLuongThe}").Append("\n \n");

//             // Original Appends with explicit \r or \r\n
//             // sb.Append("  Doanh Thu thẻ: " + doanhThuBanThe.ToString("C", cultureInfo) + "\r"); -> one \n
//             sb.Append("  Doanh Thu thẻ: " + doanhThuBanThe.ToString("C", cultureInfo)).Append("\n");
//             // sb.Append($"Số KH BSGT: {tongKhachBsgt} KH\r\n"); -> one \n
//             sb.Append($"Số KH BSGT: {tongKhachBsgt} KH").Append("\n");
//             // sb.Append($"Số KH đi cùng: {tongKhachDiCung} KH\r\n"); -> one \n
//             sb.Append($"Số KH đi cùng: {tongKhachDiCung} KH").Append("\n");

//             // Back to the double newline pattern
//             sb.Append("  2. Tổng doanh thu:  " + doanhThu.ToString("C", cultureInfo)).Append("\n\n");
//             sb.Append("- Khách lẻ:  " + tongBilKhachLe.ToString("C", cultureInfo)).Append("\n\n");
//             sb.Append("- Hợp đồng gói:  " + tongBilHopDong.ToString("C", cultureInfo)).Append("\n\n");
//             sb.Append("- Đặt trước:  " + tongBilDatTruoc.ToString("C", cultureInfo)).Append("\n \n"); // Ends with space
//             sb.Append("- Thẻ:  -  ").Append("\n \n"); // Ends with space
//             sb.Append("- Doanh thu thanh toán online:  " + doanhThuOnline.ToString("C", cultureInfo)).Append("\n \n"); // Ends with space
//             sb.Append("- Doanh thu KH sử dụng DV VIP:  " + doanhThuKhSuDungDichVuVip.ToString("C", cultureInfo))
//                 .Append("\n \n"); // Ends with space

//             sb.Append("3. Cụ thể:").Append("\n\n");
//             sb.Append("- KH nội tỉnh: ").Append("\n\n");
//             sb.Append(
//                     "- Tỉ Lệ : Sáng: "
//                         + (tongKhach > 0 ? ((float)tongSoKhachBuoiSang / tongKhach).ToString("P2", cultureInfo) : "")
//                 )
//                 .Append("\n\n");
//             sb.Append($"- KH mới: {tongSoLuotTnMoi} KH").Append("\n\n");
//             sb.Append($"- KH sử dụng DV VIP: {khSuDungDvVip} KH").Append("\n\n");
//             sb.Append($"- KH đặt trước: {soKhachDatTruoc} KH").Append("\n\n");
//             sb.Append($"- KH đặt trước không khám: {soKhachDatTruoc - soKhachDatTruocCoKham} KH ").Append("\n\n"); // Ends with space
//             sb.Append($"- KH mua HĐ không khám: {soKhachHopDong - soKhachHopDongCoKham} KH ").Append("\n\n"); // Ends with space
//             sb.Append("- KH BSGT:  " + doanhThuBsgt.ToString("C", cultureInfo)).Append("\n\n");
//             sb.Append("- KH Đi cùng:  " + doanhThuKhDiCung.ToString("C", cultureInfo)).Append("\n\n");
//             sb.Append($"- KH được tiêm: {tongSoKhachDuocTiem} KH").Append("\n\n");
//             sb.Append($"- KH không được tiêm: {tongKhachKhongDuocTiem}").Append("\n\n");
//             sb.Append("Lý do: ").Append("\n\n");
//             sb.Append($"- Số mũi tiêm: {tongSoMuiTiem}").Append("\n\n");
//             sb.Append("- Hệ số mũi tiêm:  " + heSoMuiTiem.ToString("0.00", cultureInfo)).Append("\n\n");

//             sb.Append("4. Vắc xin sử dụng:").Append("\n\n");
//             sb.Append("4.1 Vắc xin báo cáo theo yêu cầu của BTT:").Append("\n\n");
//             sb.Append(" Vắc xin cần tăng cường:").Append("\n\n"); // Note: vaccineKhuyenKhichs is on its own line
//             sb.Append(vaccineKhuyenKhichs).Append("\n\n"); // This adds an extra \n compared to how it might have been
//             sb.Append(" Vắc xin cần hạn chế:").Append("\n\n"); // Note: vaccineHanChes is on its own line
//             // Original: sb.AppendLine(vaccineHanChes + "\r\n\r");
//             // This was effectively vaccineHanChes + <newline> + <blank line> + <blank line>
//             // So, content + \n + \n + \n
//             sb.Append(vaccineHanChes).Append("\n\n\n"); // This gives content + 3 newlines

//             sb.Append("4.2 Vắc xin tiêu thụ đột biến trong ngày: ").Append("\n\n");
//             sb.Append("4.3 Vắc xin không tiêu thụ trong ngày: ").Append("\n\n");
//             sb.Append("4.4 Các TTTC lân cận").Append("\n\n"); // This line in original did not have \r
//             sb.Append("5. Hoạt động tại TT:").Append("\n\n");
//             sb.Append("- Bàn khám: 0 bàn khám/ 0 phòng khám - Chiều: 0 bàn khám/0 phòng khám").Append("\n\n");
//             sb.Append("- Bàn tiêm: Sáng: 0 bàn tiêm/ 0 phòng tiêm - Chiều: 0 bàn/0 phòng").Append("\n\n");
//             sb.Append("- Phục vụ KH: Tốt.").Append("\n\n");
//             sb.Append("6. Các vấn đề phát sinh và hành động khắc phục: ").Append("\n\n");
//             sb.Append("7. Đề xuất: không").Append("\n\n");
//             sb.Append("8. Kế hoạch ngày:   ").Append("\n\n");
//             sb.Append("- Bàn khám: 0 bàn khám/ 0 phòng khám - Chiều: 0 bàn khám/ 0 phòng khám").Append("\n\n");
//             sb.Append("- Bàn tiêm: Sáng: 0 bàn tiêm/ 0 phòng tiêm - Chiều: 0 bàn/ 0 phòng").Append("\n\n");
//             sb.Append("Trân trọng,").Append("\n\n");
//             sb.Append(customer.NguoiDaiDien).Append("\n\n");

//             dataSet.Tables.Add(new List<object> { new { MessageContent = sb.ToString() } }.ToDataTable());
//             return dataSet;
//         }

//         return @params.Type switch
//         {
//             9 => HandleType9(physicianAdmissionsQuery),
//             10 => HandleType10(@params.FacId, invApprovedOutsQuery),
//             _ => new DataSet(),
//         };
//     }

//     private DataSet HandleType9(IQueryable<PhysicianAdmissionDto> physicianAdmissionsQuery)
//     {
//         return (
//             from a in physicianAdmissionsQuery
//             from c in db
//                 .QAHosGenericDB.MdmPatients.With(SqlServerHints.Table.NoLock)
//                 .Where(c => c.PatientId == a.PatientId)
//             from d in db
//                 .QAHosGenericDB.LDepartmentRooms.With(SqlServerHints.Table.NoLock)
//                 .Where(d => d.RoomId == a.RoomId && d.FacId == a.FacId)
//             from e in db.Security.Users.With(SqlServerHints.Table.NoLock).Where(e => e.Id == a.PrimaryDoctor)
//             from f in db.HR.MdmEmployees.With(SqlServerHints.Table.NoLock).Where(f => f.EmployeeId == e.EmpId)
//             from g in db
//                 .QAHosGenericDB.CnVitalSigns.With(SqlServerHints.Table.NoLock)
//                 .Where(g =>
//                     g.PatientId == c.PatientId
//                     && g.FacAdmissionId == a.FacAdmissionId
//                     && g.PhysicianAdmissionId == a.PhysicianAdmissionId
//                 )
//             where a.IsKhongDuocTiem == true
//             orderby c.PatientHospitalId
//             select new
//             {
//                 NgayKham = a.AdmitDate.AsDate(),
//                 MaBenhNhan = c.PatientHospitalId,
//                 HovaTen = c.FullName,
//                 Phong = d.RoomName,
//                 BacSi = f.FullName,
//                 GhiChu = g.GhiChu ?? "",
//                 a.IsKhongDuocTiem,
//             }
//         )
//             .Distinct()
//             .ToDataSet();
//     }

//     private DataSet HandleType10(string facId, IQueryable<InvApprovedOutDto> invApprovedOutsQuery)
//     {
//         var dataSet = new DataSet();
//         var approvedOutForProducts = (
//             from a in invApprovedOutsQuery
//             from b in db
//                 .QAHosGenericDB.InvApprovedOutDetails.With(SqlServerHints.Table.NoLock)
//                 .Where(b => b.ApprovedOutId == a.ApprovedOutId)
//             from e in db
//                 .QAHosGenericDB.LProducts.With(SqlServerHints.Table.NoLock)
//                 .Where(e => e.ProductId == b.ProductId)
//             where e.FacId == facId && e.ProductTypeId == 17
//             select new
//             {
//                 a.ApprovedOutNo,
//                 a.RequestStockId,
//                 e.ProductName,
//                 e.ProductId,
//                 Date = a.CreatedOn.AsDate(),
//                 a.CreatedOn,
//                 b.ClinicalSessionId,
//                 b.ApprovedQty,
//             }
//         )
//             .QueryHint(SqlServerHints.Query.ForceOrder)
//             .Distinct()
//             .ToList();
//         var table1 = (
//             from a in approvedOutForProducts
//             group a by new
//             {
//                 a.ProductId,
//                 a.ProductName,
//                 a.ApprovedQty,
//             } into g
//             select new
//             {
//                 ProductID = g.Key.ProductId,
//                 g.Key.ProductName,
//                 LoaiXuat = g.Key.ApprovedQty,
//                 LuongXuat = g.Sum(g1 => g1.ApprovedQty),
//                 Sl = g.Count(),
//             }
//         )
//             .OrderBy(x => x.ProductName)
//             .ThenByDescending(x => x.Sl)
//             .ToDataTable();
//         dataSet.Tables.Add(table1);
//         var table2 = (
//             from a in approvedOutForProducts
//             group a by new { a.ProductId, a.ProductName } into g
//             select new
//             {
//                 ProductID = g.Key.ProductId,
//                 g.Key.ProductName,
//                 Sl = g.Count(),
//             }
//         )
//             .OrderByDescending(x => x.Sl)
//             .ThenBy(x => x.ProductName)
//             .ToDataTable();
//         dataSet.Tables.Add(table2);
//         return dataSet;
//     }

//     private Decimal CalcRealTotal(
//         string facId,
//         long tuNgayAsBigInt,
//         long denNgayAsBigInt,
//         int tuNgayAsInt,
//         int denNgayAsInt,
//         int checksumFacId
//     )
//     {
//         var cashesQuery = db
//             .QAHosGenericDB.BilInvoiceCashes.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 c.CreatedDateAsInt,
//                 c.CheckSumFacId,
//             });

//         var transfersQuery = db
//             .QAHosGenericDB.BilInvoiceTransfers.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 c.CreatedDateAsInt,
//                 c.CheckSumFacId,
//             });

//         var atmQuery = db
//             .QAHosGenericDB.BilInvoiceCredits.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 c.CreatedDateAsInt,
//                 c.CheckSumFacId,
//             });

//         var othersQuery = db
//             .QAHosGenericDB.BilInvoiceOthers.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 c.CreatedDateAsInt,
//                 c.CheckSumFacId,
//             });

//         var vouchersQuery = db
//             .QAHosGenericDB.BilInvoiceVouchers.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 c.CreatedDateAsInt,
//                 c.CheckSumFacId,
//             });

//         var qaPaysQuery = db
//             .QAHosGenericDB.BilInvoiceQapays.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 c.CreatedDateAsInt,
//                 c.CheckSumFacId,
//             });

//         var vnPaysQuery = db
//             .QAHosGenericDB.BilInvoiceVnpays.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 c.CreatedDateAsInt,
//                 c.CheckSumFacId,
//             });

//         var mCreditsQuery = db
//             .QAHosGenericDB.BilInvoiceMCredits.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 c.CreatedDateAsInt,
//                 c.CheckSumFacId,
//             });

//         var theTinDungsQuery = db
//             .QAHosGenericDB.BilInvoiceTheTinDungs.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 CreatedDateAsInt = (long?)(c.CreatedDateAsInt * 1_000_000L),
//                 CheckSumFacId = (int?)c.CheckSumFacId,
//             });

//         var postpaidsQuery = db
//             .QAHosGenericDB.BilInvoicePostpaids.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 c.CreatedDateAsInt,
//                 c.CheckSumFacId,
//             });

//         var techcomsQuery = db
//             .QAHosGenericDB.BilInvoiceTechcoms.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 InvoiceNo = (string?)c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 c.CreatedDateAsInt,
//                 CheckSumFacId = (int?)c.CheckSumFacId,
//             });

//         var mbsQuery = db
//             .QAHosGenericDB.BilInvoiceMbs.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 InvoiceNo = (string?)c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 c.CreatedDateAsInt,
//                 CheckSumFacId = (int?)c.CheckSumFacId,
//             });

//         var phieuMuaHangsQuery = db
//             .QAHosGenericDB.BilInvoicePhieuMuaHangs.With(SqlServerHints.Table.NoLock)
//             .Select(c => new
//             {
//                 InvoiceId = c.InvoiceIdGroup!.Value,
//                 c.InvoiceNo,
//                 c.RefundType,
//                 RealAmount = c.RealTotal ?? 0m,
//                 c.CreatedDateAsInt,
//                 c.CheckSumFacId,
//             });

//         var allPaymentsQuery = cashesQuery
//             .Concat(transfersQuery)
//             .Concat(atmQuery)
//             .Concat(othersQuery)
//             .Concat(vouchersQuery)
//             .Concat(qaPaysQuery)
//             .Concat(vnPaysQuery)
//             .Concat(mCreditsQuery)
//             .Concat(theTinDungsQuery)
//             .Concat(postpaidsQuery)
//             .Concat(techcomsQuery)
//             .Concat(mbsQuery)
//             .Concat(phieuMuaHangsQuery);

//         int ngayBangLive = settingsService.GetBilLiveDataDate(facId).DateAsInt();

//         if (tuNgayAsInt > ngayBangLive)
//         {
//             decimal totalPayment = (
//                 from payment in allPaymentsQuery
//                 join invoice in db.QAHosGenericDB.BilInvoiceLives.With(SqlServerHints.Table.NoLock)
//                     on payment.InvoiceId equals invoice.InvoiceId
//                 join tempPTTT in db.QAHosGenericDB.BilInvoiceTempForHinhThucThanhToans.With(SqlServerHints.Table.NoLock)
//                     on payment.InvoiceId equals tempPTTT.InvoiceId
//                     into tempPTTT
//                 from tempPayment in tempPTTT.DefaultIfEmpty()
//                 where
//                     invoice.CheckSumFacId == checksumFacId
//                     && !invoice.Reason!.Contains(
//                         "Lưu doanh thu vaccine lúc bấm tiêm tại phòng tiêm vaccine, đây là vật tư"
//                     )
//                     //&& !invoice.Reason!.Contains("Lưu doanh thu vaccine")
//                     && invoice.InvoiceNo != ""
//                     && invoice.CounterId != 999
//                     && payment.CheckSumFacId == checksumFacId
//                     && payment.CreatedDateAsInt >= tuNgayAsBigInt
//                     && payment.CreatedDateAsInt <= denNgayAsBigInt
//                     && payment.CheckSumFacId == checksumFacId
//                     && (tempPayment != null || invoice.InvoiceNo == payment.InvoiceNo)
//                 select payment.RefundType != null ? 0 : payment.RealAmount
//             ).Sum();

//             decimal totalNoHopDong = (
//                 from invoice in db.QAHosGenericDB.BilInvoiceLives.With(SqlServerHints.Table.NoLock)
//                 join tempPTTT in db.QAHosGenericDB.BilInvoiceTempForHinhThucThanhToans.With(SqlServerHints.Table.NoLock)
//                     on invoice.InvoiceId equals tempPTTT.InvoiceId
//                     into tempPTTT
//                 from tempPayment in tempPTTT.DefaultIfEmpty()
//                 where
//                     (invoice.HopDongId == null || invoice.IsTamUng != false)
//                     && invoice.CheckSumFacId == checksumFacId
//                     && invoice.CreatedDateAsInt >= tuNgayAsInt
//                     && invoice.CreatedDateAsInt <= denNgayAsInt
//                     && !invoice.Reason!.Contains(
//                         "Lưu doanh thu vaccine lúc bấm tiêm tại phòng tiêm vaccine, đây là vật tư"
//                     )
//                     && invoice.InvoiceNo != ""
//                     && invoice.CounterId != 999
//                 select invoice.RefundType != null ? 0
//                 : tempPayment == null ? invoice.RealTotal!.Value
//                 : 0
//             ).Sum();

//             return totalPayment + totalNoHopDong;
//         }
//         else
//         {
//             decimal totalPayment = (
//                 from payment in allPaymentsQuery
//                 join invoice in db.QAHosGenericDB.BilInvoices.With(SqlServerHints.Table.NoLock)
//                     on payment.InvoiceId equals invoice.InvoiceId
//                 join tempPTTT in db.QAHosGenericDB.BilInvoiceTempForHinhThucThanhToans.With(SqlServerHints.Table.NoLock)
//                     on payment.InvoiceId equals tempPTTT.InvoiceId
//                     into tempPTTT
//                 from tempPayment in tempPTTT.DefaultIfEmpty()
//                 where
//                     invoice.CheckSumFacId == checksumFacId
//                     && !invoice.Reason!.Contains(
//                         "Lưu doanh thu vaccine lúc bấm tiêm tại phòng tiêm vaccine, đây là vật tư"
//                     )
//                     //&& !invoice.Reason!.Contains("Lưu doanh thu vaccine")
//                     && invoice.InvoiceNo != ""
//                     && invoice.CounterId != 999
//                     && payment.CheckSumFacId == checksumFacId
//                     && payment.CreatedDateAsInt >= tuNgayAsBigInt
//                     && payment.CreatedDateAsInt <= denNgayAsBigInt
//                     && payment.CheckSumFacId == checksumFacId
//                     && (tempPayment != null || invoice.InvoiceNo == payment.InvoiceNo)
//                 select payment.RefundType != null ? 0 : payment.RealAmount
//             ).Sum();

//             decimal totalNoHopDong = (
//                 from invoice in db.QAHosGenericDB.BilInvoices.With(SqlServerHints.Table.NoLock)
//                 join tempPTTT in db.QAHosGenericDB.BilInvoiceTempForHinhThucThanhToans.With(SqlServerHints.Table.NoLock)
//                     on invoice.InvoiceId equals tempPTTT.InvoiceId
//                     into tempPTTT
//                 from tempPayment in tempPTTT.DefaultIfEmpty()
//                 where
//                     (invoice.HopDongId == null || invoice.IsTamUng != false)
//                     && invoice.CheckSumFacId == checksumFacId
//                     && invoice.CreatedDateAsInt >= tuNgayAsInt
//                     && invoice.CreatedDateAsInt <= denNgayAsInt
//                     && !invoice.Reason!.Contains(
//                         "Lưu doanh thu vaccine lúc bấm tiêm tại phòng tiêm vaccine, đây là vật tư"
//                     )
//                     && invoice.InvoiceNo != ""
//                     && invoice.CounterId != 999
//                 select invoice.RefundType != null ? 0
//                 : tempPayment == null ? invoice.RealTotal!.Value
//                 : 0
//             ).Sum();

//             return totalPayment + totalNoHopDong;
//         }
//     }
// }
