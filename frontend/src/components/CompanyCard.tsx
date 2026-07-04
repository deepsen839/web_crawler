import {
    Phone,
    MapPin,
    Building2,
    Flag,
    Download,
} from "lucide-react";

interface Company {
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

interface Props {
    company: Company;
    downloadUrl: string;
}

export default function CompanyCard({
    company,
    downloadUrl,
}: Props) {
    return (
        <div className="rounded-xl bg-white shadow-lg p-6 space-y-6">

            <div className="flex items-center justify-between">

                <div>

                    <h2 className="text-2xl font-bold">
                        {company.company_name}
                    </h2>

                    <a
                        href={company.website}
                        target="_blank"
                        rel="noreferrer"
                        className="text-blue-600 hover:underline"
                    >
                        {company.website}
                    </a>

                </div>

                <a
                    href={downloadUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
                >
                    <Download size={18} />
                    Download PDF
                </a>

            </div>

            <div className="grid md:grid-cols-2 gap-4">

                <InfoRow
                    icon={<Phone size={18} />}
                    title="Phone"
                    value={company.phone_number}
                />

                <InfoRow
                    icon={<MapPin size={18} />}
                    title="Address"
                    value={company.address}
                />

                <InfoRow
                    icon={<Building2 size={18} />}
                    title="Industry"
                    value={company.industry}
                />

                <InfoRow
                    icon={<Flag size={18} />}
                    title="Country"
                    value={company.country}
                />

            </div>

            <Section
                title="Company Summary"
            >
                <p className="text-gray-700 leading-relaxed">
                    {company.company_summary}
                </p>
            </Section>

            <Section
                title="Products & Services"
            >
                <ul className="list-disc ml-5 space-y-1">

                    {company.products_services.map((item) => (
                        <li key={item}>{item}</li>
                    ))}

                </ul>
            </Section>

            <Section
                title="AI Generated Pain Points"
            >
                <ul className="list-disc ml-5 space-y-1">

                    {company.pain_points.map((item) => (
                        <li key={item}>{item}</li>
                    ))}

                </ul>
            </Section>

        </div>
    );
}

interface InfoProps {
    icon: React.ReactNode;
    title: string;
    value: string;
}

function InfoRow({
    icon,
    title,
    value,
}: InfoProps) {
    return (
        <div className="flex gap-3 items-start rounded-lg border p-4">

            <div className="text-blue-600">
                {icon}
            </div>

            <div>

                <p className="text-sm text-gray-500">
                    {title}
                </p>

                <p className="font-medium">
                    {value || "N/A"}
                </p>

            </div>

        </div>
    );
}

interface SectionProps {
    title: string;
    children: React.ReactNode;
}

function Section({
    title,
    children,
}: SectionProps) {
    return (
        <div>

            <h3 className="mb-2 text-lg font-semibold">
                {title}
            </h3>

            {children}

        </div>
    );
}