# Chronicle FAQ

## ❓ Frequently Asked Questions

---

## General Questions

### Q: Apa itu Chronicle?
**A**: Chronicle adalah platform digital untuk manajemen pemakaman (cemetery management) yang memungkinkan organisasi pemakaman mengelola plot, burial requests, sales, dan operasional sehari-hari secara terintegrasi. Platform ini menyediakan interface web-based dengan visualisasi geospasial, tracking inventory, workflow management, dan comprehensive reporting.

---

### Q: Siapa yang bisa menggunakan Chronicle?
**A**: Chronicle dirancang untuk tiga tipe user utama:
- **Owner**: Pemilik/pengelola organisasi pemakaman dengan full access ke configuration, financial reports, dan user management
- **Admin**: Administrator untuk operasional harian, mengelola plots, requests, sales, dan organization settings
- **Manager**: Manajer lapangan untuk review dan approval burial requests, monitoring operations, dan limited reporting

Setiap role memiliki permission dan access level yang berbeda sesuai responsibilities mereka.

---

### Q: Bagaimana cara mulai menggunakan Chronicle?
**A**: 
1. **Registration**: Owner mendaftar organization melalui registration page atau menerima invitation
2. **Setup**: Configure organization settings, cemeteries, sections/lots, pricing, dan custom fields
3. **Add Users**: Invite Admin dan Manager via email invitation system
4. **Start Using**: Login ke dashboard dan mulai manage plots, requests, sales sesuai role

Untuk detail lengkap, lihat [flow.md](flow.md) untuk product flow dan [roles/](roles/README.md) untuk role-specific guides.

---

### Q: Apa perbedaan antara Owner, Admin, dan Manager?
**A**: 

| Aspek | Owner | Admin | Manager |
|-------|-------|-------|---------|
| **Access Level** | Full access | Administrative | Operational |
| **Organization Config** | ✅ Full | ✅ Full | ❌ |
| **User Management** | ✅ | ✅ | ❌ |
| **Plot Management** | ✅ Full | ✅ Full | ✅ View Only |
| **Request Approval** | ✅ | ✅ | ✅ |
| **Sales Management** | ✅ | ✅ | ❌ |
| **Financial Reports** | ✅ All | ✅ All | ✅ Limited |
| **Custom Fields/Forms** | ✅ | ✅ | ❌ |

---

## Features & Functionality

### Q: Apa fitur utama Chronicle?
**A**: Fitur utama Chronicle meliputi:
- **Multi-View Dashboard**: Map view, Tables view, Calendar view untuk visualisasi data berbeda
- **Plot Management**: Track inventory dari vacant hingga occupied dengan lifecycle management
- **Request Management**: Workflow system untuk burial requests dari submission hingga completion
- **Sales & Revenue**: Track plot sales, payments, invoice generation, dan financial analytics
- **Interactive Mapping**: Geospatial visualization dengan satellite imagery dan plot markers
- **Organization Config**: Centralized settings untuk cemeteries, access control, pricing, custom fields
- **Reporting**: Comprehensive reports dengan customizable metrics dan multiple export formats
- **Calendar**: Event scheduling untuk burials, ceremonies, dan maintenance

Lihat [features.md](features.md) untuk detail lengkap setiap fitur.

---

### Q: Bagaimana cara kerja Map View?
**A**: Map View menyediakan dual-pane interface:
- **Left Pane**: Statistics cards dengan metrics (Total Plots, Occupied, Vacant, Interments)
- **Right Pane**: Interactive satellite map dengan vector overlays untuk sections/lots

User bisa pan/zoom map, click pada plots untuk details, dan visually identify available inventory. Map view sangat helpful untuk customer interactions saat selecting plot locations.

---

### Q: Apakah Chronicle support custom fields?
**A**: Ya! Chronicle menyediakan Custom Field Builder dimana Owner/Admin bisa define custom data fields untuk plots, requests, dan sales. 

**Capabilities**:
- Multiple field types (text, number, date, dropdown, checkbox)
- Validation rules
- Required/optional settings
- Conditional visibility
- Integration dengan forms dan reports

Navigate ke **Organization > Custom Fields** untuk setup.

---

### Q: Bagaimana proses burial request?
**A**: Burial request workflow:

```
1. Submit Request → Family/funeral home submit request dengan documents
2. Document Verification → System validate required documents
3. Manager Review → Manager review request dan documents
4. Approval Decision → Approve atau reject request
5. Schedule Burial → If approved, schedule date di calendar
6. Execute Burial → Conduct burial ceremony
7. Update Records → Mark plot as occupied, generate certificate
```

System send email notifications di setiap stage dan track status real-time.

---

### Q: Bisakah manage multiple cemeteries dalam satu organization?
**A**: Ya! Chronicle support multi-cemetery management. Owner bisa setup multiple cemetery locations dalam Organization > Cemeteries, dengan:
- Separate configurations per cemetery
- Per-cemetery analytics dan reports
- Location-specific pricing
- Cemetery switcher dalam interface
- Consolidated reporting across all cemeteries

---

## Technical Questions

### Q: Platform apa saja yang didukung?
**A**: Chronicle tersedia sebagai:
- **Web Application**: Full-featured browser-based interface
- **Browser Support**: Chrome, Firefox, Safari, Edge (latest versions)
- **Responsive Design**: Optimized untuk desktop, tablet, dan mobile devices
- **No Installation**: Access langsung via web browser, no desktop app needed

---

### Q: Bagaimana dengan keamanan data?
**A**: Chronicle implement security measures:
- **Authentication**: Encrypted password storage, social login support (Google, Microsoft)
- **Session Management**: Secure session handling dengan "Remember me" option
- **Role-Based Access Control**: Granular permissions based on user role
- **Data Encryption**: Secure data transmission dan storage
- **Password Recovery**: Secure password reset flow

---

### Q: Apakah Chronicle menyediakan API?
**A**: Chronicle dirancang sebagai web application dengan browser-based interface. Untuk integration needs atau API access, hubungi support team untuk discuss custom integration requirements.

---

### Q: Format export apa yang didukung?
**A**: Chronicle support multiple export formats:
- **PDF**: Reports, certificates, documents
- **Excel**: Data exports untuk analysis
- **CSV**: Bulk data exports
- **iCal/Google Calendar**: Calendar events integration

---

## Account & Access

### Q: Bagaimana cara login ke Chronicle?
**A**: Chronicle menyediakan multiple authentication methods:
1. **Google Login**: OAuth dengan Google account
2. **Microsoft Login**: OAuth dengan Microsoft account
3. **Email/Password**: Chronicle account dengan email dan password

Pilih preferred method di login page, enter credentials, dan click LOGIN. Gunakan "Remember me" untuk skip login di future sessions.

---

### Q: Lupa password, bagaimana reset?
**A**: 
1. Di login page, click "Forgot password?"
2. Enter your email address
3. Check email untuk password reset link
4. Click link dan set new password
5. Login dengan new password

Password reset link valid untuk limited time (24 hours).

---

### Q: Bagaimana cara invite user baru?
**A**: (Owner/Admin only)
1. Navigate ke **Organization > Access**
2. Click **Invite User** atau similar button
3. Enter email address dan select role (Admin atau Manager)
4. Click **Send Invitation**
5. User receives email dengan invitation link
6. User clicks link, sets up account dan password
7. User automatically granted access based on assigned role

---

### Q: Bisa mengubah role user yang sudah ada?
**A**: Ya, Owner/Admin bisa modify user roles:
1. Navigate ke **Organization > Access**
2. Find user dalam user list
3. Edit user details atau permissions
4. Change role assignment
5. Save changes

Note: Changing roles immediately updates user's access permissions.

---

## Usage & Workflows

### Q: Bagaimana cara add plot baru?
**A**: (Owner/Admin)
1. Navigate ke **Dashboard > Tables** view
2. Click **Add Plot** atau similar action button
3. Fill plot details:
   - Section/Lot
   - Plot number
   - Size
   - Pricing
   - Custom fields (if configured)
4. Save plot
5. Plot appears dalam inventory sebagai "Vacant" status

Alternatively, define plots dalam **Organization > Cemeteries** untuk bulk or section-based setup.

---

### Q: Bagaimana track plot yang reserved?
**A**: Plots dengan status "Reserved" visible dalam:
- **Dashboard > Tables**: Filter by Status = Reserved
- **Map View**: Reserved plots indicated dengan color-coding
- **Sales Module**: Linked to sales records

Setup filters untuk "Reserved" plots dengan reservation date untuk track expiring reservations dan follow-up.

---

### Q: Bagaimana generate reports?
**A**: 
1. Navigate ke **Dashboard > Reports**
2. Select report type:
   - Inventory Reports (availability, occupancy)
   - Financial Reports (revenue, sales, payments)
   - Operational Reports (burials, requests)
   - Custom Reports (user-defined)
3. Set parameters (date range, filters, metrics)
4. Preview report
5. Export to PDF or Excel

Save frequently-used report configurations untuk quick access.

---

### Q: Bisakah customize certificates?
**A**: Ya! (Owner/Admin)
1. Navigate ke **Organization > Certificates**
2. Create atau edit certificate template
3. Design layout dengan merge fields (name, date, plot, etc.)
4. Setup digital signature (optional)
5. Save template

Certificates auto-generate dari burial records dan bisa batch-created atau individually issued.

---

## Troubleshooting

### Q: Kenapa tidak bisa login?
**A**: Troubleshooting steps:
1. **Check credentials**: Verify email dan password are correct
2. **Check authentication method**: Ensure using correct method (Google/Microsoft/Email)
3. **Clear browser cache**: Sometimes cached data causes issues
4. **Try password reset**: If forgot password, use password reset flow
5. **Check browser**: Try different browser atau incognito mode
6. **Contact support**: If still issues, contact system administrator

---

### Q: Plot tidak muncul di map view, kenapa?
**A**: Possible reasons:
1. **Plot coordinates not set**: Ensure plot has latitude/longitude defined
2. **Filter active**: Check if filters excluding the plot
3. **Zoom level**: Map might be zoomed too far out
4. **Cache issue**: Refresh page (Ctrl+F5 atau Cmd+Shift+R)

Verify plot details dalam Tables View untuk ensure plot configured correctly.

---

### Q: Notification email tidak terkirim, bagaimana?
**A**: Check:
1. **Email settings**: Organization > General > Notification preferences
2. **Spam folder**: Email might be filtered to spam
3. **Email address**: Verify email address correct dalam user profile
4. **System status**: Check if notification system operational

Contact system administrator if persistent issues.

---

### Q: Bagaimana cara export bulk data?
**A**: 
1. Navigate to data view (e.g., Dashboard > Tables untuk plots)
2. Apply filters if needed untuk specific data subset
3. Look for **Export** button or action
4. Select export format (CSV for bulk data)
5. Download exported file

For large datasets, export might take few moments to generate.

---

## Best Practices

### Q: Apa best practice untuk setup organization baru?
**A**: Recommended setup sequence:
1. **Organization Settings**: Configure name, contact, operating hours
2. **Cemeteries**: Define cemetery locations dan boundaries
3. **Sections/Lots**: Setup plot sections dengan pricing
4. **Custom Fields**: Define any custom data fields needed
5. **Event Types**: Configure burial types dan ceremony categories
6. **Forms**: Setup burial request forms
7. **Certificates**: Create certificate templates
8. **Users**: Invite Admin dan Manager staff
9. **Test Workflow**: Run through complete burial request workflow untuk verify setup

---

### Q: Tips untuk efficient plot inventory management?
**A**: Best practices:
1. **Regular audits**: Weekly review vacant/reserved plots
2. **Saved filters**: Create filters untuk common queries (e.g., Expiring Reservations)
3. **Custom fields**: Use custom fields untuk track additional plot attributes
4. **Map annotations**: Add ROI markers untuk planned expansions
5. **Export regularly**: Backup inventory data via exports

---

### Q: How to optimize for customer interactions?
**A**: Recommendations:
1. **Use Map View**: Visual selection easier untuk customers
2. **Prepare filters**: Pre-filter available plots in customer's budget range
3. **Show options**: Display 3-5 plot options dengan different locations/pricing
4. **Print reports**: Export plot details dengan photos untuk customer take-home
5. **Quick reservation**: Be ready untuk reserve plot immediately if customer decides

---

## 💡 Tidak Menemukan Jawaban?

Jika pertanyaan Anda tidak ada di sini:

1. **Check documentasi lengkap**: 
   - [flow.md](flow.md) - Chronicle product flow dan workflows
   - [features.md](features.md) - Detailed feature documentation
   - [roles/](roles/README.md) - Role-specific user journeys

2. **Role-specific questions**: 
   - [Owner Guide](roles/owner.md)
   - [Admin Guide](roles/admin.md)
   - [Manager Guide](roles/manager.md)

3. **Contact support**: Reach out ke system administrator atau support team

---

**Last Updated**: February 2026
