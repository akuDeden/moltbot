# Chronicle Features

## ✨ Feature Overview

Chronicle menyediakan platform lengkap untuk manajemen pemakaman digital dengan fitur-fitur yang dirancang untuk Owner, Admin, dan Manager dalam mengelola operasional pemakaman secara efisien.

---

## 🎯 Core Features

### 1. Multi-View Dashboard

**Deskripsi**: Dashboard interaktif dengan berbagai mode tampilan untuk visualisasi data yang berbeda.

**Benefit**:
- Fleksibilitas dalam melihat data sesuai kebutuhan
- Visualisasi geospasial untuk plot cemetery
- Quick access ke metrics penting
- Real-time data updates

**Mode Tampilan**:
1. **Map View**: Visualisasi satelit dengan overlay plot locations
2. **Tables View**: Data grid dengan sorting, filtering, dan search
3. **Calendar View**: Event scheduling dan timeline management

**Cara Menggunakan**:
1. Login ke Chronicle dashboard
2. Pilih view mode dari tab navigation (Map/Tables/Calendar)
3. Interact dengan data sesuai mode yang dipilih
4. Switch antar mode untuk perspektif berbeda

**Contoh Use Case**:
> Owner ingin melihat occupancy rate cemetery. Dengan Map View, owner bisa visualize plot yang occupied vs vacant. Lalu switch ke Tables View untuk drill-down ke specific plot details dan export data untuk reporting.

---

### 2. Plot Management

**Deskripsi**: Sistem manajemen komprehensif untuk mengelola plot/lot cemetery dari vacant hingga occupied.

**Benefit**:
- Track inventory plot secara real-time
- Manage lifecycle plot (Vacant → Reserved → Occupied)
- Quick identification plot availability
- Integrated dengan sales dan requests

**Key Capabilities**:
- Status tracking (Vacant, Reserved, Occupied, Maintenance)
- Plot attributes (size, location, pricing, section)
- Bulk operations
- Custom field definitions
- Search dan filtering

**Contoh Use Case**:
> Admin menerima inquiry dari customer tentang plot availability di Section A. Dengan Tables View, admin bisa filter plot yang Vacant di Section A, check pricing, dan reserve untuk customer.

---

### 3. Request Management System

**Deskripsi**: Workflow management untuk burial requests dari submission hingga completion.

**Benefit**:
- Streamline burial approval process
- Document verification
- Multi-level review
- Status tracking
- Notification system

**Request Workflow**:
```
Submit Request → Review Documents → Manager Approval → Schedule → Execute → Complete
```

**Features**:
- Request submission form
- Document upload
- Approval/rejection workflow
- Comments dan notes
- Email notifications
- Calendar integration

**Contoh Use Case**:
> Family submit burial request dengan death certificate. Manager review documents, approve request, schedule burial date di calendar, dan system automatically update plot status to Occupied setelah burial completed.

---

### 4. Sales & Revenue Tracking

**Deskripsi**: Comprehensive sales management untuk plot sales, payments, dan revenue analytics.

**Benefit**:
- Track plot sales dan revenue
- Payment processing
- Invoice generation
- Financial reporting
- Customer records

**Key Features**:
- Plot sales recording
- Payment tracking (Paid, Pending, Partial)
- Invoice generation dan templates
- Revenue analytics
- Customer database
- Sales reports

**Contoh Use Case**:
> Owner ingin review monthly revenue. Melalui Sales dashboard, owner bisa lihat total sales, pending payments, dan generate sales report untuk accounting purposes.

---

### 5. Interactive Mapping

**Deskripsi**: Geospatial visualization dengan satellite imagery dan interactive plot markers.

**Benefit**:
- Visual representation plot locations
- Easy navigation cemetery layout
- Region of Interest (ROI) markers
- Zoom dan pan functionality
- Real-time plot status overlay

**Map Features**:
- Satellite base map
- Vector overlays untuk sections/lots
- Color-coded plot status
- Clickable plot markers
- ROI definition tools
- Export map views

**Contoh Use Case**:
> Customer ingin memilih plot location. Admin bisa show interactive map, zoom ke specific section, highlight available plots dengan color-coding, dan let customer visually select preferred location.

---

### 6. Organization Configuration

**Deskripsi**: Centralized settings hub untuk configure organization, cemeteries, access control, dan preferences.

**Benefit**:
- Customizable untuk kebutuhan specific organization
- Multi-cemetery support
- Granular access control
- Flexible configuration
- Custom fields dan forms

**Configuration Modules**:

#### General Settings
- Organization name, contact, logo
- Operating hours
- Notification preferences

#### Cemetery Management
- Multiple cemetery locations
- Cemetery-specific settings
- Plot layout configuration

#### Access Control
- User invitations
- Role assignments (Owner, Admin, Manager)
- Permission management

#### Custom Fields
- Define custom data fields
- Field types dan validation
- Visibility controls

#### Sales Settings
- Pricing models
- Payment methods
- Tax configuration
- Invoice templates

#### Event Types
- Burial types
- Ceremony categories
- Custom events

#### Regional Settings
- Language preferences
- Date/time formats
- Currency
- Timezone

#### Certificates
- Certificate templates
- Digital signatures
- Auto-generation

#### Form Builder
- Custom forms
- Data collection templates
- Submission workflows

**Contoh Use Case**:
> Owner setup new cemetery location. Melalui Organization Config, owner bisa add new cemetery, define sections/lots, set pricing per section, configure custom fields untuk specific data requirements, dan setup access control untuk staff.

---

### 7. Reporting & Analytics

**Deskripsi**: Comprehensive reporting system dengan customizable reports dan analytics.

**Benefit**:
- Data-driven decision making
- Financial insights
- Occupancy analytics
- Custom report builder
- Multiple export formats

**Report Types**:
- **Inventory Reports**: Plot availability, occupancy rates, section utilization
- **Financial Reports**: Revenue, sales, payments, outstanding balances
- **Operational Reports**: Burials per period, request status, maintenance records
- **Custom Reports**: User-defined metrics dan dimensions

**Export Formats**:
- PDF documents
- Excel spreadsheets
- CSV data files

**Contoh Use Case**:
> Owner perlu quarterly report untuk board meeting. Melalui Reports module, owner bisa generate comprehensive report dengan occupancy stats, revenue breakdown, burial count, dan export ke PDF untuk presentation.

---

### 8. Calendar & Event Scheduling

**Deskripsi**: Integrated calendar system untuk schedule burials, events, dan maintenance.

**Benefit**:
- Prevent scheduling conflicts
- Visual timeline planning
- Reminder notifications
- Multi-view (Month, Week, Day)
- Resource coordination

**Calendar Features**:
- Event creation dan editing
- Burial scheduling
- Ceremony planning
- Maintenance scheduling
- Color-coded event types
- Drag-and-drop rescheduling
- Email reminders

**Contoh Use Case**:
> Manager perlu schedule burial untuk next week. Check Calendar View untuk available dates, create burial event dengan details (time, plot, family contact), dan system send notification ke relevant staff.

---

### 9. User & Access Management

**Deskripsi**: Role-based access control dengan invitation system untuk manage users.

**Benefit**:
- Granular permission control
- Secure access
- Easy onboarding
- Role separation
- Audit trail

**User Roles**:

| Role | Access Level | Key Permissions |
|------|--------------|-----------------|
| **Owner** | Full Access | All features, org config, user management, financial data |
| **Admin** | Administrative | Daily operations, requests, sales, reports, org config |
| **Manager** | Operational | Request approval, monitoring, limited reports |

**Invitation Flow**:
1. Owner/Admin send email invitation
2. User receives invitation link
3. User sets up account dan password
4. Access granted based on assigned role

**Contoh Use Case**:
> Owner hire new manager untuk cemetery operations. Owner invite manager via email, manager setup account, dan automatically get Manager-level access untuk review requests dan monitor operations.

---

### 10. Search & Filtering

**Deskripsi**: Powerful search dan filtering across all data entities.

**Benefit**:
- Quick data discovery
- Advanced filters
- Multi-criteria search
- Saved filters
- Export filtered results

**Search Capabilities**:
- Global search bar
- Entity-specific searches (plots, requests, sales)
- Text search
- Status filters
- Date range filters
- Custom field filters
- Combined filters

**Contoh Use Case**:
> Admin perlu find semua Reserved plots di Section B yang expire dalam 30 hari. Using advanced filters, admin set criteria (Status=Reserved, Section=B, Reservation Date < 30 days ago) dan get filtered list untuk follow-up.

---

## 🔧 Advanced Features

### Custom Field Builder

**Untuk siapa**: Organizations dengan unique data requirements

**Capabilities**:
- Define custom data fields untuk plots, requests, sales
- Multiple field types (text, number, date, dropdown, checkbox)
- Validation rules
- Required/optional settings
- Conditional visibility

**Setup Requirements**:
- Owner atau Admin access
- Navigate to Organization > Custom Fields
- Define field specifications

---

### Form Builder

**Untuk siapa**: Organizations yang need custom data collection workflows

**Capabilities**:
- Drag-and-drop form designer
- Custom field integration
- Multi-page forms
- Submission workflows
- Email notifications on submission

**Setup Requirements**:
- Owner atau Admin access
- Organization > Forms configuration
- Define form structure dan workflow

---

### Certificate Generation

**Untuk siapa**: Organizations issuing official burial certificates

**Capabilities**:
- Custom certificate templates
- Auto-population dari burial records
- Digital signatures
- PDF generation
- Batch certificate creation

**Setup Requirements**:
- Certificate templates configured
- Digital signature setup (if required)
- Burial data completeness

---

### Multi-Cemetery Management

**Untuk siapa**: Organizations managing multiple cemetery locations

**Capabilities**:
- Separate cemetery configurations
- Per-cemetery analytics
- Consolidated reporting
- Location-specific pricing
- Cemetery switcher dalam interface

**Setup Requirements**:
- Owner setup dalam Organization > Cemeteries
- Define cemetery locations dan boundaries
- Configure per-cemetery settings

---

## 📊 Feature Comparison by Role

| Feature | Owner | Admin | Manager |
|---------|-------|-------|---------|
| Dashboard (Map, Tables, Calendar) | ✅ | ✅ | ✅ |
| Plot Management | ✅ Full | ✅ Full | ✅ View Only |
| Request Management | ✅ | ✅ | ✅ |
| Request Approval | ✅ | ✅ | ✅ |
| Sales Management | ✅ | ✅ | ❌ |
| Reports | ✅ All | ✅ All | ✅ Limited |
| Organization Config | ✅ | ✅ | ❌ |
| User Management | ✅ | ✅ | ❌ |
| Custom Fields | ✅ | ✅ | ❌ |
| Form Builder | ✅ | ✅ | ❌ |
| Certificates | ✅ | ✅ | ❌ |
| Profile Management | ✅ | ✅ | ✅ |

---

## 🎨 UI/UX Features

### Design System
- Clean, professional interface
- Dual-pane layouts untuk data + visualization
- Responsive design (desktop, tablet, mobile)
- Dark/light mode aware
- Accessible color schemes

### Navigation
- Sidebar menu dengan kategorisasi
- Top bar dengan quick actions
- Breadcrumb navigation
- Context-aware toolbars
- Global search

### Customization
- Customizable dashboard widgets
- Saved filter presets
- Personalized views
- Column selection dalam tables
- Layout preferences

---

## 📱 Platform-Specific Features

### Web Features
- Full-featured browser interface
- No installation required
- Cross-browser compatibility (Chrome, Firefox, Safari, Edge)
- Responsive layouts
- Offline support untuk critical features (upcoming)

### Export & Integration
- PDF export untuk reports dan certificates
- Excel export untuk data analysis
- CSV export untuk bulk data
- Calendar integration (iCal, Google Calendar)
- Email notifications

---

## 💡 Tips & Best Practices

### Tip 1: Leverage Map View untuk Customer Interactions
Gunakan Map View saat interacting dengan customers untuk plot selection. Visual representation membantu customers understand plot locations dan make informed decisions.

### Tip 2: Set Up Custom Fields Early
Define custom fields di awal setup untuk ensure consistent data capture across all plots dan requests. Ini avoid data gaps dan facilitate reporting.

### Tip 3: Use Filtering untuk Operational Efficiency
Save frequently-used filter combinations untuk quick access. Misalnya, filter untuk "Expired Reservations" atau "Pending Approvals" bisa save time daily operations.

### Tip 4: Regular Report Reviews
Schedule regular (weekly/monthly) report reviews untuk monitor trends, identify issues early, dan make data-driven decisions.

### Tip 5: Utilize Calendar Integration
Integrate Calendar View dengan team calendars untuk prevent scheduling conflicts dan ensure all staff aware of upcoming burials dan events.

---

## 📚 Related Documentation

- [flow.md](flow.md) - Understand how features fit into the overall Chronicle flow
- [faq.md](faq.md) - Common questions about features
- [roles/](roles/README.md) - Role-specific feature usage dan workflows

---

**Last Updated**: February 2026
