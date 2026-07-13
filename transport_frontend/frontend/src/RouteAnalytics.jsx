import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer } from 'recharts';
import API_BASE_URL from './api';

const RouteAnalytics = ({ routeId }) => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAnalytics = async () => {
            try {
                // Ensure your Django server is running!
                const response = await axios.get(`${API_BASE_URL}/analytics/route/${routeId}/`);
                setData(response.data);
                setLoading(false);
            } catch (error) {
                console.error("Error fetching AI data:", error);
                setLoading(false);
            }
        };
        fetchAnalytics();
    }, [routeId]);

    if (loading) return <div className="p-4 text-center">Loading AI Predictions...</div>;
    if (!data) return <div className="p-4 text-center">No data available for this route.</div>;

    return (
        <div className="p-6 bg-white rounded-lg shadow-md">
            <h2 className="mb-2 text-2xl font-bold text-gray-800">Demand Forecast</h2>
            <p className="mb-6 text-blue-600 font-medium">{data.route_name}</p>
            
            <div style={{ width: '100%', height: 300 }}>
                <ResponsiveContainer>
                    <BarChart data={data.predictions}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} />
                        <XAxis dataKey="day" />
                        <YAxis title="Predicted Seats" />
                        <Tooltip 
                            contentStyle={{ borderRadius: '10px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                        />
                        <Bar dataKey="predicted_seats" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                    </BarChart>
                </ResponsiveContainer>
            </div>

            <div className="mt-6 grid grid-cols-1 gap-4">
                {data.predictions.map((p, idx) => (
                    <div key={idx} className="flex justify-between items-center p-3 bg-gray-50 rounded border-l-4 border-blue-500">
                        <span>{p.date} ({p.day})</span>
                        <span className={`font-bold ${p.status === 'High' ? 'text-red-500' : 'text-green-600'}`}>
                            {p.predicted_seats} Seats — {p.status}
                        </span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default RouteAnalytics;