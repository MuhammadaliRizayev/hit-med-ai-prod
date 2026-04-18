"use client"

import type {
  EpendymomaPayload,
  MedulloblastomaPayload,
  PatientDetail,
  PineoblastomaPayload,
  ProtocolMeta,
  ResolvedData,
} from "@/types"

type TimelineItem = {
  label: string
  value: string
  tone?: "default" | "success" | "warning" | "danger"
}

type PatientDetailDrawerProps = {
  open: boolean
  onClose: () => void
  patientDetail?: PatientDetail | null
  resolvedData?: ResolvedData | null
  integratedDiagnosis?: string | null
  clinicalNotes?: string | null
  timeline?: TimelineItem[]
  loading?: boolean
}

function cn(...items: Array<string | false | null | undefined>) {
  return items.filter(Boolean).join(" ")
}

function formatValue(value?: string | number | null, fallback = "—") {
  if (value === null || value === undefined) return fallback
  const text = String(value).trim()
  return text ? text : fallback
}

function formatSex(value?: string | null) {
  if (value === "male") return "Erkak"
  if (value === "female") return "Ayol"
  return "—"
}

function toneClasses(tone?: TimelineItem["tone"]) {
  switch (tone) {
    case "success":
      return "border-emerald-500/20 bg-emerald-500/10 text-emerald-300"
    case "warning":
      return "border-amber-500/20 bg-amber-500/10 text-amber-300"
    case "danger":
      return "border-rose-500/20 bg-rose-500/10 text-rose-300"
    default:
      return "border-slate-800 bg-slate-950 text-slate-200"
  }
}

function Panel({
  title,
  subtitle,
  children,
}: {
  title: string
  subtitle?: string
  children: React.ReactNode
}) {
  return (
    <section className="rounded-3xl border border-slate-800 bg-slate-900/80 p-5 shadow-xl shadow-black/20">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-slate-100">{title}</h3>
        {subtitle ? <p className="mt-1 text-sm text-slate-400">{subtitle}</p> : null}
      </div>
      {children}
    </section>
  )
}

function InfoCard({
  label,
  value,
}: {
  label: string
  value?: string | number | null
}) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4">
      <p className="text-xs uppercase tracking-wide text-slate-500">{label}</p>
      <p className="mt-2 text-sm font-medium text-slate-100">{formatValue(value)}</p>
    </div>
  )
}

function extractDiseasePayload(
  patientDetail?: PatientDetail | null,
):
  | MedulloblastomaPayload
  | EpendymomaPayload
  | PineoblastomaPayload
  | null
  | undefined {
  const disease = patientDetail?.diagnosis?.disease

  if (disease === "medulloblastoma") return patientDetail?.medulloblastoma
  if (disease === "ependymoma") return patientDetail?.ependymoma
  if (disease === "pineoblastoma") return patientDetail?.pineoblastoma

  return null
}

function buildDiseaseRows(patientDetail?: PatientDetail | null) {
  const disease = patientDetail?.diagnosis?.disease
  const payload = extractDiseasePayload(patientDetail)

  if (!disease || !payload) return []

  if (disease === "medulloblastoma") {
    const data = payload as MedulloblastomaPayload
    return [
      { label: "Histology", value: data.histology },
      { label: "Genetics", value: data.genetics },
      { label: "Methylation class", value: data.methylationClass },
      { label: "M status", value: data.mStatus },
      { label: "R status", value: data.rStatus },
    ]
  }

  const data = payload as EpendymomaPayload | PineoblastomaPayload
  return [
    { label: "Histology", value: data.histology },
    { label: "Methylation class", value: data.methylationClass },
    { label: "Location", value: data.location },
    { label: "M status", value: data.mStatus },
    { label: "R status", value: data.rStatus },
  ]
}

function buildProtocolMeta(
  protocol?: ProtocolMeta | null,
  resolvedData?: ResolvedData | null,
) {
  return {
    tableId: resolvedData?.tableId || protocol?.tableId || "—",
    riskGroup: protocol?.riskGroup || "—",
    phase: protocol?.phase || "—",
    status: protocol?.status || "—",
    reviewRequired: resolvedData?.reviewRequired ?? protocol?.reviewRequired ?? false,
    justification:
      resolvedData?.explanation?.length
        ? resolvedData.explanation
        : protocol?.justification?.length
          ? protocol.justification
          : [],
  }
}

export default function PatientDetailDrawer({
  open,
  onClose,
  patientDetail,
  resolvedData,
  integratedDiagnosis,
  clinicalNotes,
  timeline = [],
  loading = false,
}: PatientDetailDrawerProps) {
  const protocol = buildProtocolMeta(patientDetail?.protocol, resolvedData)
  const diseaseRows = buildDiseaseRows(patientDetail)

  return (
    <>
      <div
        className={cn(
          "fixed inset-0 z-40 bg-black/60 backdrop-blur-sm transition-opacity duration-300",
          open ? "pointer-events-auto opacity-100" : "pointer-events-none opacity-0",
        )}
        onClick={onClose}
      />

      <aside
        className={cn(
          "fixed right-0 top-0 z-50 h-screen w-full max-w-3xl overflow-y-auto border-l border-slate-800 bg-slate-950 text-slate-100 shadow-2xl shadow-black/40 transition-transform duration-300",
          open ? "translate-x-0" : "translate-x-full",
        )}
        aria-hidden={!open}
      >
        <div className="sticky top-0 z-20 border-b border-slate-800 bg-slate-950/95 backdrop-blur">
          <div className="flex items-start justify-between gap-4 px-6 py-5">
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-cyan-400">
                Patient Workspace
              </p>
              <h2 className="mt-2 text-2xl font-semibold text-slate-100">
                {patientDetail?.patient?.lastName || patientDetail?.patient?.firstName
                  ? `${patientDetail?.patient?.lastName || ""} ${patientDetail?.patient?.firstName || ""}`.trim()
                  : "Bemor tafsilotlari"}
              </h2>
              <p className="mt-2 text-sm text-slate-400">
                Clinical profile, diagnosis, protocol va kuzatuv ma&apos;lumotlari
              </p>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="rounded-2xl border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-medium text-slate-300 transition hover:border-slate-600 hover:bg-slate-800 hover:text-white"
            >
              Yopish
            </button>
          </div>
        </div>

        <div className="space-y-6 px-6 py-6">
          {loading ? (
            <div className="flex min-h-[320px] items-center justify-center rounded-3xl border border-slate-800 bg-slate-900/60">
              <div className="text-center">
                <div className="mx-auto h-10 w-10 animate-spin rounded-full border-b-2 border-cyan-400" />
                <p className="mt-4 text-sm text-slate-400">Bemor ma&apos;lumotlari yuklanmoqda...</p>
              </div>
            </div>
          ) : (
            <>
              <Panel title="Patient info" subtitle="Shaxsiy va antropometrik ma&apos;lumotlar">
                <div className="grid gap-4 md:grid-cols-2">
                  <InfoCard label="Familiya" value={patientDetail?.patient?.lastName} />
                  <InfoCard label="Ism" value={patientDetail?.patient?.firstName} />
                  <InfoCard label="Otasining ismi" value={patientDetail?.patient?.middleName} />
                  <InfoCard label="Tug'ilgan sana" value={patientDetail?.patient?.birthDate} />
                  <InfoCard label="Jins" value={formatSex(patientDetail?.patient?.sex)} />
                  <InfoCard label="Bo'y" value={patientDetail?.anthropometry?.heightCm ? `${patientDetail.anthropometry.heightCm} sm` : "—"} />
                  <InfoCard label="Vazn" value={patientDetail?.anthropometry?.weightKg ? `${patientDetail.anthropometry.weightKg} kg` : "—"} />
                  <InfoCard label="BSA" value={patientDetail?.anthropometry?.bsa ? `${patientDetail.anthropometry.bsa.toFixed(2)} m²` : "—"} />
                </div>
              </Panel>

              <Panel title="Diagnosis" subtitle="Tashxis va subspecialty parametrlar">
                <div className="space-y-4">
                  <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4">
                    <p className="text-xs uppercase tracking-wide text-slate-500">Kasallik turi</p>
                    <p className="mt-2 text-lg font-semibold text-cyan-400">
                      {formatValue(patientDetail?.diagnosis?.disease)}
                    </p>
                  </div>

                  <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4">
                    <p className="text-xs uppercase tracking-wide text-slate-500">
                      Integrated diagnosis
                    </p>
                    <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-200">
                      {formatValue(
                        integratedDiagnosis || patientDetail?.diagnosis?.integratedSummary,
                      )}
                    </p>
                  </div>

                  {diseaseRows.length > 0 ? (
                    <div className="grid gap-4 md:grid-cols-2">
                      {diseaseRows.map((row) => (
                        <InfoCard key={row.label} label={row.label} value={row.value} />
                      ))}
                    </div>
                  ) : (
                    <div className="rounded-2xl border border-amber-500/20 bg-amber-500/10 p-4 text-sm text-amber-300">
                      Tashxisning chuqur parametrlarini ko&apos;rsatish uchun mos disease payload topilmadi.
                    </div>
                  )}
                </div>
              </Panel>

              <Panel title="Protocol table" subtitle="Aniqlangan jadval va klinik status">
                <div className="grid gap-4 md:grid-cols-2">
                  <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/10 p-4">
                    <p className="text-xs uppercase tracking-wide text-emerald-400">Table ID</p>
                    <p className="mt-2 text-2xl font-bold text-emerald-300">
                      {protocol.tableId}
                    </p>
                  </div>

                  <div
                    className={cn(
                      "rounded-2xl border p-4",
                      protocol.reviewRequired
                        ? "border-amber-500/20 bg-amber-500/10"
                        : "border-cyan-500/20 bg-cyan-500/10",
                    )}
                  >
                    <p
                      className={cn(
                        "text-xs uppercase tracking-wide",
                        protocol.reviewRequired ? "text-amber-400" : "text-cyan-400",
                      )}
                    >
                      Review status
                    </p>
                    <p
                      className={cn(
                        "mt-2 text-lg font-semibold",
                        protocol.reviewRequired ? "text-amber-300" : "text-cyan-300",
                      )}
                    >
                      {protocol.reviewRequired ? "Manual review kerak" : "Review talab qilinmaydi"}
                    </p>
                  </div>

                  <InfoCard label="Risk group" value={protocol.riskGroup} />
                  <InfoCard label="Phase" value={protocol.phase} />
                  <InfoCard label="Status" value={protocol.status} />
                </div>
              </Panel>

              <Panel title="Justification" subtitle="Jadval tanlash asoslari">
                {protocol.justification.length > 0 ? (
                  <div className="space-y-3">
                    {protocol.justification.map((item, index) => (
                      <div
                        key={`${item}-${index}`}
                        className="rounded-2xl border border-slate-800 bg-slate-950 p-4"
                      >
                        <div className="flex gap-3">
                          <div className="mt-0.5 flex h-6 w-6 items-center justify-center rounded-full bg-cyan-500/15 text-xs font-semibold text-cyan-300">
                            {index + 1}
                          </div>
                          <p className="text-sm leading-6 text-slate-200">{item}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4 text-sm text-slate-400">
                    Justification ma&apos;lumotlari hozircha mavjud emas.
                  </div>
                )}
              </Panel>

              <Panel title="Clinical notes" subtitle="Qo&apos;shimcha klinik izohlar">
                <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4">
                  <p className="whitespace-pre-wrap text-sm leading-6 text-slate-200">
                    {formatValue(clinicalNotes)}
                  </p>
                </div>
              </Panel>

              <Panel title="Timeline" subtitle="Jarayonning asosiy bosqichlari">
                {timeline.length > 0 ? (
                  <div className="space-y-3">
                    {timeline.map((item, index) => (
                      <div
                        key={`${item.label}-${index}`}
                        className={cn(
                          "rounded-2xl border p-4",
                          toneClasses(item.tone),
                        )}
                      >
                        <div className="flex items-start gap-3">
                          <div className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full border border-current/20 bg-black/10 text-xs font-semibold">
                            {index + 1}
                          </div>
                          <div>
                            <p className="text-sm font-semibold">{item.label}</p>
                            <p className="mt-1 text-sm opacity-90">{item.value}</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="rounded-2xl border border-slate-800 bg-slate-950 p-4 text-sm text-slate-400">
                    Timeline ma&apos;lumotlari hali shakllanmagan.
                  </div>
                )}
              </Panel>
            </>
          )}
        </div>
      </aside>
    </>
  )
}