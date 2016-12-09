from enum import Enum

JOB_TYPES = ['Administrative & Mgmt', 'Administrative Secretarial', 'Administrative-DPW/PUC', 'Administrative-Labor & Trades', 'Agriculture & Horticulture', 'Airport Operation', 'Appraisal & Taxation', 'Budget Admn & Stats Analysis', 'Clerical Secretarial & Steno', 'Community Development', 'Computer Operatns & Repro Svcs', 'Construction Inspection', 'Construction Project Mgmt', 'Correction & Detention', 'Dietary & Food', 'Emergency Services', 'Energy & Environment', 'Fire Services', 'Health & Sanitation Inspection', 'Hospital Administration', 'Housekeeping & Laundry', 'Human Services', 'Information Systems', 'Journeyman Trade', 'Lab Pharmacy & Med Techs', 'Legal & Court', 'Library', 'Management', 'Med Therapy & Auxiliary', 'Medical & Dental', 'Museum & Cultural Affairs', 'Nursing', 'Park & Zoo', 'Payroll Billing & Accounting', 'Personnel', 'Police Services', 'Port Operation', 'Probation & Parole', 'Professional Engineering', 'Property Administration', 'Protection & Apprehension', 'Pub Relations & Spec Assts', 'Public Health', 'Public Safety Inspection', 'Public Service Aide', 'Purchasing & Storekeeping', 'Recreation', 'Revenue', 'SF Redevelopment Agency', 'SF Superior Court', 'Semi-Skilled & General Labor', 'Skilled Labor', 'Street Transit', 'Sub-Professional Engineering', 'Supervisory-Labor & Trade']


class Strategy(Enum):
    accept_first = 1
    reject_first_accept_second = 2
    randomly_accept = 3
    negotiate_until_satisfied = 4
    negotiate_once = 5


class Action(Enum):
    propose = 1
    nothing = 2
    accept = 4
