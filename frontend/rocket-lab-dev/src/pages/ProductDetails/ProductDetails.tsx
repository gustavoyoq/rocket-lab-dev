import { useMemo, type ReactNode } from 'react'
import { FaAngleLeft } from 'react-icons/fa'
import { Link, useParams } from 'react-router-dom'
import { Button } from '../../components/ui/Button'
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

function formatPriceBrl(value: number | null | undefined) {
  if (value === null || value === undefined) {
    return 'Preço não disponível'
  }

  return value.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
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
        <Button variant="secondary" asChild>
          <Link to="/">Voltar para o catálogo</Link>
        </Button>
      </StateBox>
    )
  }

  return (
    <section className="mx-auto max-w-6xl space-y-6">
      <div className="flex items-center justify-between gap-4">
        <Button variant="secondary" asChild>
          <Link to="/">
            <span className="inline-flex items-center gap-1">
              <FaAngleLeft aria-hidden="true" />
              Voltar para o catálogo
            </span>
          </Link>
        </Button>
      </div>

      <article className="overflow-hidden rounded-4xl bg-[#a4ef8e] ring-1 ring-[#99d98c]">
        <div className="grid gap-0 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="min-h-112 bg-[#a4ef8e] p-5 lg:p-6">
            <div className="flex h-full min-h-96 items-center justify-center overflow-hidden rounded-3xl bg-[#a4ef8e] p-4">
              {product.imagem_url ? (
                <img src={product.imagem_url} alt={product.nome_produto} className="h-full w-full rounded-2xl object-cover" />
              ) : (
                <div className="flex h-full min-h-80 w-full items-center justify-center rounded-2xl bg-[#a4ef8e] text-lg font-semibold text-slate-500">
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

              <div className="grid gap-3 text-sm text-slate-700 sm:grid-cols-2 lg:grid-cols-3">
                <InfoItem label="Vendas" value={`${product.salesCount}`} size="large" />
                <InfoItem label="Avaliação média" value={formatRating(product.averageRating)} size="large" />
                <InfoItem label="Preço estimado" value={formatPriceBrl(product.estimatedPriceBrl)} size="large" />
              </div>

              <div className="rounded-3xl bg-[#99d98c] px-4 py-4 ring-1 ring-[#99d98c]">
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-slate-500">Propriedades</p>
                <div className="mt-3 space-y-2 text-sm text-slate-700">
                  <p><span className="font-semibold text-slate-900">Peso:</span> {formatValue(product.peso_produto_gramas, ' g')}</p>
                  <p><span className="font-semibold text-slate-900">Comprimento:</span> {formatValue(product.comprimento_centimetros, ' cm')}</p>
                  <p><span className="font-semibold text-slate-900">Altura:</span> {formatValue(product.altura_centimetros, ' cm')}</p>
                  <p><span className="font-semibold text-slate-900">Largura:</span> {formatValue(product.largura_centimetros, ' cm')}</p>
                </div>
              </div>
            </div>


          </div>
        </div>
      </article>

      <article className="overflow-hidden rounded-4xl bg-[#a4ef8e] ring-1 ring-[#99d98c] p-6 lg:p-8">
          <div className="flex items-center justify-between gap-4">
            <h3 className="text-xl font-semibold text-slate-900">Avaliações do produto</h3>
            <span className="text-sm text-slate-500">{product.reviewCount} comentários associados</span>
          </div>

          {reviews.length === 0 ? (
            <div className="mt-4 rounded-2xl border border-dashed border-[#99d98c] bg-[#a4ef8e] px-4 py-6 text-sm text-slate-700">
              Nenhuma avaliação relacionada encontrada para este produto.
            </div>
          ) : (
            <div className="mt-4 grid gap-4 md:grid-cols-2 xl:grid-cols-3">
              {reviews.map((review) => (
                <article key={review.id_avaliacao} className="rounded-2xl bg-[#d9ff77] p-4">
                  <p className="text-sm font-semibold text-[#6b8f4a]">Nota: {review.avaliacao}</p>
                  <h4 className="mt-2 text-base font-semibold text-slate-900">{review.titulo_comentario ?? 'Sem título'}</h4>
                  <p className="mt-2 text-sm leading-6 text-slate-600">{review.comentario ?? 'Sem comentário'}</p>
                </article>
              ))}
            </div>
          )}
      </article>

      <article className="overflow-hidden rounded-4xl bg-[#a4ef8e] ring-1 ring-[#99d98c] p-6 lg:p-8">
        <h3 className="text-xl font-semibold text-slate-900">Produtos similares</h3>

        {similarLoading ? (
          <div className="mt-4 rounded-2xl border border-dashed border-[#99d98c] bg-[#a4ef8e] px-4 py-6 text-sm text-slate-700">
            Carregando produtos similares...
          </div>
        ) : topSimilarProducts.length === 0 ? (
          <div className="mt-4 rounded-2xl border border-dashed border-[#99d98c] bg-[#a4ef8e] px-4 py-6 text-sm text-slate-700">
            Nenhum produto similar encontrado.
          </div>
        ) : (
          <div className="mt-4 grid gap-3 grid-cols-2 md:grid-cols-3 lg:grid-cols-5">
            {topSimilarProducts.map((item) => (
              <article key={item.id_produto} className="group relative overflow-hidden rounded-3xl border border-[#99d98c] bg-[#a4ef8e] transition">
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

function InfoItem({
  label,
  value,
  size = 'default',
}: {
  label: string
  value: string
  size?: 'default' | 'large'
}) {
  return (
    <div className={`rounded-2xl bg-[#99d98c] px-4 py-3 ring-1 ring-[#99d98c] ${size === 'large' ? 'py-4' : ''}`}>
      <p className={`uppercase tracking-[0.16em] text-slate-500 ${size === 'large' ? 'text-sm' : 'text-xs'}`}>{label}</p>
      <p className={`mt-1 font-semibold text-slate-900 ${size === 'large' ? 'text-2xl' : 'text-base'}`}>{value}</p>
    </div>
  )
}

function StateBox({ children, variant = 'default' }: { children: ReactNode; variant?: 'default' | 'error' }) {
  return (
    <div
      className={`flex min-h-[60vh] flex-col items-center justify-center gap-4 rounded-3xl border px-6 py-10 text-center shadow-sm ${
        variant === 'error' ? 'border-rose-200 bg-rose-50 text-rose-700' : 'border-[#99d98c] bg-[#a4ef8e] text-slate-800'
      }`}
    >
      {children}
    </div>
  )
}
