# class CurrentStatusService:
#     def __init__(self, user):
#         self.user = user
#
#     def get_total_available(self):
#         """Calculate total available money for specific user"""
#         base_query = Transaction.objects.filter(user=self.user)
#
#         if self.user.is_superuser:
#             base_query = Transaction.objects.all()
#
#         income = base_query.filter(
#             transaction_type__type='income'
#         ).aggregate(
#             total=Coalesce(Sum('amount'), 0)
#         )['total']
#
#         expenses = base_query.filter(
#             transaction_type__type='expense'
#         ).aggregate(
#             total=Coalesce(Sum('amount'), 0)
#         )['total']
#
#         return {
#             'total_available': income - expenses,
#             'total_income': income,
#             'total_expenses': expenses
#         }
#
#     def get_location_distribution(self):
#         """Get money distribution by location for specific user"""
#         base_query = Location.objects
#
#         if not self.user.is_superuser:
#             base_query = base_query.filter(user=self.user)
#
#         return base_query.annotate(
#             total_income=Coalesce(Sum(
#                 'transactions__amount',
#                 filter=Q(
#                     transactions__transaction_type__type='income',
#                     transactions__user=self.user
#                 )
#             ), 0),
#             total_expenses=Coalesce(Sum(
#                 'transactions__amount',
#                 filter=Q(
#                     transactions__transaction_type__type='expense',
#                     transactions__user=self.user
#                 )
#             ), 0),
#             available=F('total_income') - F('total_expenses')
#         ).values('name', 'total_income', 'total_expenses', 'available')
#
#     def get_bucket_distribution(self):
#         """Get money distribution by bucket for specific user"""
#         base_query = Bucket.objects
#
#         if not self.user.is_superuser:
#             base_query = base_query.filter(user=self.user)
#
#         return base_query.annotate(
#             total_income=Coalesce(Sum(
#                 'transactions__amount',
#                 filter=Q(
#                     transactions__transaction_type__type='income',
#                     transactions__user=self.user
#                 )
#             ), 0),
#             total_expenses=Coalesce(Sum(
#                 'transactions__amount',
#                 filter=Q(
#                     transactions__transaction_type__type='expense',
#                     transactions__user=self.user
#                 )
#             ), 0),
#             available=F('total_income') - F('total_expenses')
#         ).values('name', 'total_income', 'total_expenses', 'available')