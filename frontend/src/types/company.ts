export interface Company {
    company_name: string;
    website: string;

    phone_number: string;
    address: string;

    industry: string;
    country: string;

    company_summary: string;

    products_services: string[];

    pain_points: string[];
}

export interface Competitor {
    name: string;
    website: string;
    source: string;
}

export interface ResearchResponse {
    company: Company;

    competitors: Competitor[];

    crawled_pages: number;

    download_url: string;
}

export interface ResearchRequest {
    company: string;

    applicant_name: string;

    applicant_email: string;

    model: string;
}