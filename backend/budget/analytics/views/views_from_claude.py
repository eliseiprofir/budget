# class CurrentStatusViewSet(ViewSet):
#     permission_classes = [IsAuthenticated]
#
#     def get_service(self):
#         """Initialize service with current user"""
#         return CurrentStatusService(self.request.user)
#
#     @action(detail=False, methods=['GET'])
#     def summary(self, request):
#         """Get complete current status summary"""
#         try:
#             service = self.get_service()
#             data = {
#                 'totals': service.get_total_available(),
#                 'locations': service.get_location_distribution(),
#                 'buckets': service.get_bucket_distribution()
#             }
#             return Response(data)
#         except ValidationError as e:
#             return Response({'error': str(e)}, status=400)
#         except Exception as e:
#             return Response({'error': str(e)}, status=500)
#
#     @action(detail=False, methods=['GET'])
#     def totals(self, request):
#         try:
#             service = self.get_service()
#             data = service.get_total_available()
#             return Response(data)
#         except Exception as e:
#             return Response({'error': str(e)}, status=500)