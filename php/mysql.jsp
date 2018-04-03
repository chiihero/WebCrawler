<%@page import="org.json.*"%>
<%@ page language="java" import="java.util.*" pageEncoding="UTF-8"%>
<%@ page language="java" import="java.sql.*"%>
<%
	request.setCharacterEncoding("UTF-8");
%>
<%
	response.setHeader("Access-Control-Allow-Methods", "OPTIONS,POST,GET");
	response.setHeader("Access-Control-Allow-Headers", "x-requested-with,content-type");
	response.setHeader("Access-Control-Allow-Origin", "*");
	//删除
	String driver = "com.mysql.jdbc.Driver";
	String url = "jdbc:mysql://139.199.11.57:3306/webcrawler?";

	Connection conn = null;
	Statement stmt = null;
	String sql;
	try {
		Class.forName(driver);
		conn = DriverManager.getConnection(url, "webcrawler", "webcrawler1");
		stmt = conn.createStatement();
		//out.println("MYSQL");
		String action = request.getParameter("display");	//得到行为


		/*显示评论*/
		//out.println(action);
		/*select and display*/
		sql = "select link,title,tag,type,author,source from picture_info order by id asc limit "+action+"";
		ResultSet rs = stmt.executeQuery(sql);
		//生成一个JSON类 这个类在jsp中显示
		JSONObject commentJson = new JSONObject();
		//生成一个JSON类
		List commentList = new ArrayList();
		while(rs.next()){
		//	out.println(rs.getInt(1) + "&nbsp; &nbsp;" + rs.getString(2));
			JSONObject Pinglun = new JSONObject();
			Pinglun.put("link",rs.getString(1));
			Pinglun.put("title",rs.getString(2));
			Pinglun.put("tag",rs.getString(3));
			Pinglun.put("type",rs.getString(4));
			Pinglun.put("author",rs.getString(5));
			Pinglun.put("source",rs.getString(6));
			commentList.add(Pinglun);
		}
		
		commentJson.put("comments",commentList);//http 访问的接口名字comments
		out.print(commentJson);
		out.flush();
		stmt.close();
		conn.close();
	} catch (SQLException e) {
		out.println("MySQL操作错误！");
		e.printStackTrace();
	} catch (Exception e) {
		out.println("MySQL操作错误！请传入正确的值！ ");
		e.printStackTrace();
	}
%>
