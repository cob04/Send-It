

class TestParcelUserOrderEndpoints:
 
    def test_fetching_all_orders(self, init_db, client, token):
        """Test endpoint to return all parcels for a user."""
        with app.context():
            response = client.get("/api/v3/parcels", headers=token())
            assert response.status_code == 200
