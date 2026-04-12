import type { OrderItem, Product, ProductListingItem, ProductReview } from '../types/product'

function calculateAverage(reviews: ProductReview[]): number {
  if (reviews.length === 0) {
    return 0
  }

  const total = reviews.reduce((sum, review) => sum + review.avaliacao, 0)
  return total / reviews.length
}

export function enrichProductsWithMetrics(
  products: Product[],
  orderItems: OrderItem[],
  reviews: ProductReview[],
): ProductListingItem[] {
  const salesCountByProduct = new Map<string, number>()
  const ordersByProduct = new Map<string, Set<string>>()
  const reviewsByOrder = new Map<string, ProductReview[]>()

  for (const item of orderItems) {
    salesCountByProduct.set(item.id_produto, (salesCountByProduct.get(item.id_produto) ?? 0) + 1)

    const orderSet = ordersByProduct.get(item.id_produto) ?? new Set<string>()
    orderSet.add(item.id_pedido)
    ordersByProduct.set(item.id_produto, orderSet)
  }

  for (const review of reviews) {
    const currentReviews = reviewsByOrder.get(review.id_pedido) ?? []
    currentReviews.push(review)
    reviewsByOrder.set(review.id_pedido, currentReviews)
  }

  return products.map((product) => {
    const orderIds = ordersByProduct.get(product.id_produto) ?? new Set<string>()
    const productReviews = Array.from(orderIds).flatMap((orderId) => reviewsByOrder.get(orderId) ?? [])

    return {
      ...product,
      salesCount: salesCountByProduct.get(product.id_produto) ?? 0,
      averageRating: calculateAverage(productReviews),
      reviewCount: productReviews.length,
    }
  })
}

export function enrichProductWithMetrics(
  product: Product,
  orderItems: OrderItem[],
  reviews: ProductReview[],
): ProductListingItem {
  const enrichedProducts = enrichProductsWithMetrics([product], orderItems, reviews)
  return enrichedProducts[0]
}
