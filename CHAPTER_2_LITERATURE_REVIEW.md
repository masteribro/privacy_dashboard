# Chapter 2: Literature Review

## 2.1 Introduction
This chapter reviews existing literature on personal data management, privacy regulations, and related systems. It examines the theoretical foundations, regulatory frameworks, and existing solutions that inform the design of the Privacy Dashboard application.

## 2.2 Privacy Regulations and Legal Frameworks

### 2.2.1 General Data Protection Regulation (GDPR)
The GDPR (EU Regulation 2016/679) is the primary data protection regulation for the European Union and the European Economic Area. Key provisions relevant to this project include:

**Article 7 - Consent Requirements:**
- Consent must be freely given, specific, informed, and unambiguous
- Users have the right to withdraw consent at any time
- The burden of proof lies with the organization collecting data

**Article 15 - Right of Access:**
- Users have the right to obtain confirmation of whether data is being processed
- Users can request access to their personal data
- Organizations must provide this data in a structured, commonly used format (data portability)

**Article 20 - Right to Data Portability:**
- Users can receive their data in a structured, machine-readable format
- Users can transmit this data to another controller without hindrance
- Essential for user autonomy and freedom of choice

**Article 33 & 34 - Breach Notification:**
- Data breaches must be reported to authorities within 72 hours
- Users must be informed without undue delay if risks are identified

### 2.2.2 California Consumer Privacy Act (CCPA)
The CCPA (California Civil Code §1798.100 et seq.) provides California residents with specific privacy rights:

**Key Rights:**
- Right to know what personal information is collected
- Right to delete collected personal data
- Right to opt-out of the sale or sharing of personal information
- Right to non-discrimination for exercising privacy rights

**Relevance to Dashboard:**
- Information disclosure about data collection practices
- User control over data sharing preferences
- Opt-out mechanisms for data sales

### 2.2.3 Nigeria Data Protection Regulation (NDPR)
The NDPR (2019) by the National Information Technology Development Agency (NITDA) is Nigeria's primary data protection framework:

**Key Provisions:**
- Organizations must obtain explicit consent before processing personal data
- Individuals have rights to access, correct, and delete their data
- Data must be processed fairly and lawfully
- Organizations must implement appropriate security measures

**Application to This Project:**
- Particularly relevant for Nigerian users of the dashboard
- Emphasizes user consent and data rights management
- Requires transparent data handling practices

## 2.3 Personal Data Management Systems

### 2.3.1 Existing Solutions
Several existing systems provide personal data management capabilities:

**Apple Privacy Dashboard (2021):**
- Shows which apps have accessed user data
- Displays permission usage patterns
- Allows users to revoke permissions
- Limitation: Limited to Apple ecosystem only

**Google My Activity:**
- Centralizes data from all Google services
- Shows search history, location data, videos watched
- Allows bulk deletion of activity
- Limitation: Only covers Google services, limited portability

**AWS Data Portal:**
- Allows organizations to view their data usage
- Provides data export capabilities
- Complex interface not designed for individual users

### 2.3.2 Gap in Existing Solutions
Current solutions lack:
1. **Multi-organization aggregation** - Most systems focus on single organizations
2. **Unified consent management** - No single system manages consents across services
3. **Privacy scoring** - Limited visual indicators of privacy risk
4. **Data flow visualization** - Users don't understand how data moves between services
5. **Accessibility** - Difficult for average users to understand complex privacy settings

## 2.4 Data Privacy and User Control

### 2.4.1 Privacy by Design Principle
Privacy by Design (Cavoukian, 2009) proposes that privacy must be embedded into system design from the outset:

**Seven Foundational Principles:**
1. Proactive not Reactive - Prevent privacy breaches before they occur
2. Privacy as Default - Default settings should be privacy-protective
3. Privacy Embedded in Design - Integrated throughout architecture
4. Full Functionality - Achieve privacy and business objectives simultaneously
5. End-to-End Protection - Secure throughout data lifecycle
6. Visibility and Transparency - Operations open to scrutiny
7. User-Centric - User autonomy and control prioritized

**Application:** The Privacy Dashboard implements Privacy by Design by giving users visibility and control over their data, transparent consent mechanisms, and privacy scoring.

### 2.4.2 Consent Management
Modern consent management requires:

**Clear Consent Mechanisms:**
- Explicit, granular consent for specific purposes
- Easy withdrawal of consent
- Timestamp recording of consent
- Audit trails for compliance

**Informed Decision-Making:**
- Users understand what they are consenting to
- Clear language about data usage purposes
- Visibility into who is accessing their data

## 2.5 Data Visualization and Privacy Indicators

### 2.5.1 Importance of Visualization
Research shows that users struggle to understand privacy policies and settings. Data visualization helps by:

**Making Privacy Tangible:**
- Visual representations of collected data
- Privacy scores and risk indicators
- Data flow diagrams showing information movement
- Color-coded sensitivity levels

### 2.5.2 Privacy Scoring Metrics
The dashboard implements a privacy health score based on:

**Factors:**
1. **Number of organizations** - More organizations = higher risk
2. **Consent status** - Active consents lower the score
3. **Data sensitivity** - Financial/health data weighted more heavily
4. **Data retention** - Older data has lower impact

**Formula:**
```
Privacy Score = Base Score (70) + Consent Adjustment + Organization Penalty
```

## 2.6 Related Technologies and Frameworks

### 2.6.1 Web Application Frameworks
**Flask:**
- Lightweight Python web framework
- Ideal for rapid development of data-driven applications
- Built-in security features (CSRF protection, secure cookies)
- Excellent for educational projects

### 2.6.2 Database Technologies
**SQLite:**
- Lightweight, file-based relational database
- Ideal for prototyping and single-user applications
- Good for storing structured personal data
- Limited for high-concurrency scenarios

### 2.6.3 Frontend Technologies
**Bootstrap 5:**
- Responsive design framework
- Pre-built components for data visualization
- Accessibility features built-in
- Reduces development time

## 2.7 Audit Logging and Compliance

### 2.7.1 Importance of Audit Logs
Regulatory compliance requires maintaining audit trails that show:
- What data was accessed and when
- Who accessed the data
- What actions were performed
- Success or failure status

**GDPR Requirement:**
- Organizations must maintain records of processing activities
- Users should have visibility into who accessed their data

### 2.7.2 Audit Log Implementation
The dashboard tracks:
- User login/logout events
- Data view access
- Consent changes
- Data export requests
- Privacy setting modifications

## 2.8 Summary
This literature review established:

1. **Regulatory Framework** - GDPR, CCPA, and NDPR require user consent and data control
2. **Gap in Market** - Existing solutions don't provide unified personal data management
3. **Privacy by Design** - Systems should embed privacy from the start
4. **User Needs** - Users need visualization and control over their data
5. **Technical Foundation** - Flask, SQLite, and Bootstrap provide suitable technology stack

The Privacy Dashboard addresses these gaps by providing a user-centric system that aggregates personal data from multiple organizations, visualizes privacy risks, and enables granular consent management.
