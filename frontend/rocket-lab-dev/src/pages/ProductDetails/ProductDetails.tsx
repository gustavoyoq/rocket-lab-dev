import { useMemo, type ReactNode } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useProductDetails } from '../../hooks/useProductDetails'
import { getCategoryLabel } from '../../lib/category'

function formatValue(value: number | null | undefined, suffix = '') {
  if (value === null || value === undefined) {
    return 'N/A'
  }

  return `${value}${suffix}`
}

function formatRating(value: number) {
  if (value === 0) {
    return 'Sem avaliação'
  }

  return value.toFixed(1)
}

export function ProductDetails() {
  const { productId } = useParams<{ productId: string }>()
  const { product, reviews, similarProducts, similarLoading, loading, error } = useProductDetails(productId)
  const sortedSimilarProducts = useMemo(
    () =>
      [...similarProducts].sort((left, right) => {
        if (right.averageRating !== left.averageRating) {
          return right.averageRating - left.averageRating
        }

        if (right.reviewCount !== left.reviewCount) {
          return right.reviewCount - left.reviewCount
        }

        return left.nome_produto.localeCompare(right.nome_produto, 'pt-BR', { sensitivity: 'base' })
      }),
    [similarProducts],
  )
  const topSimilarProducts = useMemo(() => sortedSimilarProducts.slice(0, 5), [sortedSimilarProducts])

  if (loading) {
    return <StateBox>Carregando detalhes do produto...</StateBox>
  }

  if (error || !product) {
    return (
      <StateBox variant="error">
        <p>{error ?? 'Produto nao encontrado.'}</p>
        <Link
          to="/"
          className="inline-flex items-center justify-center rounded-xl bg-slate-100 px-4 py-2 text-sm font-medium text-slate-800 transition hover:bg-slate-200"
        >
          Voltar para o catálogo
        </Link>
      </StateBox>
    )
  }

  return (
    <section className="mx-auto max-w-6xl space-y-6">
      <div className="flex items-center justify-between gap-4">
        <Link className="text-sm font-medium text-slate-600 transition hover:text-slate-900" to="/">
          ← Voltar para o catálogo
        </Link>
      </div>

      <article className="overflow-hidden rounded-4xl bg-[#b5e48c] ring-1 ring-[#99d98c]">
        <div className="grid gap-0 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="min-h-112 bg-[#b5e48c] p-5 lg:p-6">
            <div className="flex h-full min-h-96 items-center justify-center overflow-hidden rounded-3xl bg-[#b5e48c] p-4">
              {product.imagem_url ? (
                <img src={product.imagem_url} alt={product.nome_produto} className="h-full w-full rounded-2xl object-cover" />
              ) : (
                <div className="flex h-full min-h-80 w-full items-center justify-center rounded-2xl bg-[#b5e48c] text-lg font-semibold text-slate-500">
                  Sem imagem disponível
                </div>
              )}
            </div>
          </div>

          <div className="flex flex-col justify-between gap-6 p-6 lg:p-8">
            <div className="space-y-10">
              <div>
                <p className="text-sm font-medium uppercase tracking-[0.2em] text-[#6b8f4a]">{getCategoryLabel(product.categoria_produto)}</p>
                <h2 className="mt-2 text-3xl font-semibold text-slate-900">{product.nome_produto}</h2>
              </div>

              <div className="grid gap-3 text-sm text-slate-700 sm:grid-cols-2">
                <InfoItem label="Vendas" value={`${product.salesCount}`} />
                <InfoItem label="Avaliação média" value={formatRating(product.averageRating)} />
                <InfoItem label="Peso" value={formatValue(product.peso_produto_gramas, ' g')} />
                <InfoItem label="Comprimento" value={formatValue(product.comprimento_centimetros, ' cm')} />
                <InfoItem label="Altura" value={formatValue(product.altura_centimetros, ' cm')} />
                <InfoItem label="Largura" value={formatValue(product.largura_centimetros, ' cm')} />
              </div>
            </div>


          </div>
        </div>
      </article>

      <article className="overflow-hidden rounded-4xl bg-[#b5e48c] ring-1 ring-[#99d98c] p-6 lg:p-8">
          <div className="flex items-center justify-between gap-4">
            <h3 className="text-xl font-semibold text-slate-900">Avaliações do produto</h3>
            <span className="text-sm text-slate-500">{product.reviewCount} comentários associados</span>
          </div>

          {reviews.length === 0 ? (
            <div className="mt-4 rounded-2xl border border-dashed border-[#99d98c] bg-[#b5e48c] px-4 py-6 text-sm text-slate-700">
              Nenhuma avaliação relacionada encontrada para este produto.
            </div>
          ) : (
            <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {reviews.map((review) => (
                <article key={review.id_avaliacao} className="rounded-2xl border border-[#99d98c] bg-[#d9ed92] p-4 shadow-sm">
                  <p className="text-sm font-semibold text-[#6b8f4a]">Nota: {review.avaliacao}</p>
                  <h4 className="mt-2 text-base font-semibold text-slate-900">{review.titulo_comentario ?? 'Sem título'}</h4>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{review.comentario ?? 'Sem comentário'}</p>
                </article>
              ))}
            </div>
          )}
      </article>

      <article className="overflow-hidden rounded-4xl bg-[#b5e48c] ring-1 ring-[#99d98c] p-6 lg:p-8">
        <h3 className="text-xl font-semibold text-slate-900">Produtos similares</h3>

        {similarLoading ? (
          <div className="mt-4 rounded-2xl border border-dashed border-[#99d98c] bg-[#b5e48c] px-4 py-6 text-sm text-slate-700">
            Carregando produtos similares...
          </div>
        ) : topSimilarProducts.length === 0 ? (
          <div className="mt-4 rounded-2xl border border-dashed border-[#99d98c] bg-[#b5e48c] px-4 py-6 text-sm text-slate-700">
            Nenhum produto similar encontrado.
          </div>
        ) : (
          <div className="mt-4 grid gap-3 grid-cols-2 md:grid-cols-3 lg:grid-cols-5">
            {topSimilarProducts.map((item) => (
              <article key={item.id_produto} className="group relative overflow-hidden rounded-3xl border border-[#99d98c] bg-[#b5e48c] transition">
                <Link to={`/produtos/${item.id_produto}`} className="block">
                  <div className="h-28 overflow-hidden bg-slate-100">
                    {item.imagem_url ? (
                      <img src={item.imagem_url} alt={item.nome_produto} className="h-full w-full object-cover transition duration-300 group-hover:scale-105" loading="lazy" />
                    ) : (
                      <div className="flex h-full items-center justify-center bg-linear-to-br from-slate-200 to-slate-100 text-xs font-medium text-slate-500">
                        Sem imagem
                      </div>
                    )}
                  </div>
                </Link>

                <Link to={`/produtos/${item.id_produto}`} className="block px-3 py-3 text-left">
                  <h4 className="h-10 overflow-hidden text-sm font-semibold text-slate-900">{item.nome_produto}</h4>
                  <div className="mt-2 flex items-end justify-between gap-2">
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-xs text-slate-500">{getCategoryLabel(item.categoria_produto)}</p>
                      <p className="mt-1 text-[11px] text-slate-400">{item.salesCount} vendas</p>
                    </div>
                    <div className={`shrink-0 rounded-full px-2 py-0.5 text-xs font-semibold ${item.averageRating > 0 ? 'bg-amber-100 text-amber-700' : 'bg-slate-200 text-slate-600'}`}>
                      {item.averageRating > 0 ? `★ ${formatRating(item.averageRating)}` : formatRating(item.averageRating)}
                    </div>
                  </div>
                </Link>
              </article>
            ))}
          </div>
        )}
      </article>
    </section>
  )
}

function InfoItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-[#99d98c] px-4 py-3 ring-1 ring-[#99d98c]">
      <p className="text-xs uppercase tracking-[0.16em] text-slate-500">{label}</p>
      <p className="mt-1 font-semibold text-slate-900">{value}</p>
    </div>
  )
}

function StateBox({ children, variant = 'default' }: { children: ReactNode; variant?: 'default' | 'error' }) {
  return (
    <div
      className={`flex min-h-[60vh] flex-col items-center justify-center gap-4 rounded-3xl border px-6 py-10 text-center shadow-sm ${
        variant === 'error' ? 'border-rose-200 bg-rose-50 text-rose-700' : 'border-[#99d98c] bg-[#b5e48c] text-slate-800'
      }`}
    >
      {children}
    </div>
  )
}
